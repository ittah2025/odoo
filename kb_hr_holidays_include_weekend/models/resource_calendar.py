import itertools
from odoo import api, models, _
from odoo.addons.resource.models.resource import Intervals, float_to_time
from odoo.exceptions import AccessError, UserError, ValidationError

from pytz import timezone
from datetime import datetime
from odoo.osv import expression
from collections import defaultdict
from pytz import timezone, utc
from dateutil.rrule import rrule, DAILY, WEEKLY

class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'
    
    # rewrite _attendance_intervals_batch method, base odoo module
    def _weekend_intervals(self, start_dt, end_dt, resources=None, domain=None, tz=None):
        assert start_dt.tzinfo and end_dt.tzinfo
        self.ensure_one()

        if not resources:
            resources = self.env['resource.resource']
            resources_list = [resources]
        else:
            resources_list = list(resources) + [self.env['resource.resource']]
        resource_ids = [r.id for r in resources_list]
        domain = domain if domain is not None else []
        domain = expression.AND([domain, [
            ('calendar_id', '=', self.id),
            ('resource_id', 'in', resource_ids),
            ('display_type', '=', False),
        ]])

        attendances = self.env['resource.calendar.attendance'].search(domain)
        # Since we only have one calendar to take in account
        # Group resources per tz they will all have the same result
        resources_per_tz = defaultdict(list)
        for resource in resources_list:
            resources_per_tz[tz or timezone((resource or self).tz)].append(resource)
        # Resource specific attendances
        attendance_per_resource = defaultdict(lambda: self.env['resource.calendar.attendance'])
        # Calendar attendances per day of the week
        # * 7 days per week * 2 for two week calendars
        attendances_per_day = [self.env['resource.calendar.attendance']] * 7 * 2
        weekdays = set()
        for attendance in attendances:
            if attendance.resource_id:
                attendance_per_resource[attendance.resource_id] |= attendance
            weekday = int(attendance.dayofweek)
            weekends = {d for d in range(7) if d not in weekdays}
            weekdays.add(weekday)
            weekdays.update(weekends)
            if self.two_weeks_calendar:
                weektype = int(attendance.week_type)
                attendances_per_day[weekday + 7 * weektype] |= attendance
            else:
                attendances_per_day[weekday] |= attendance
                attendances_per_day[weekday + 7] |= attendance

        start = start_dt.astimezone(utc)
        end = end_dt.astimezone(utc)
        bounds_per_tz = {
            tz: (start_dt.astimezone(tz), end_dt.astimezone(tz))
            for tz in resources_per_tz.keys()
        }
        # Use the outer bounds from the requested timezones
        for tz, bounds in bounds_per_tz.items():
            start = min(start, bounds[0].replace(tzinfo=utc))
            end = max(end, bounds[1].replace(tzinfo=utc))
        # Generate once with utc as timezone
        days = rrule(DAILY, start.date(), until=end.date(), byweekday=weekdays)

        base_result = []
        per_resource_result = defaultdict(list)
        for day in days:
            day_from = datetime.combine(day, float_to_time(attendance.hour_from))
            day_to = datetime.combine(day, float_to_time(attendance.hour_to))
            base_result.append((day_from, day_to, attendance))


        # Copy the result localized once per necessary timezone
        # Strictly speaking comparing start_dt < time or start_dt.astimezone(tz) < time
        # should always yield the same result. however while working with dates it is easier
        # if all dates have the same format
        result_per_tz = {
            tz: [(max(bounds_per_tz[tz][0], tz.localize(val[0])),
                min(bounds_per_tz[tz][1], tz.localize(val[1])),
                val[2])
                    for val in base_result]
            for tz in resources_per_tz.keys()
        }
        result_per_resource_id = dict()
        for tz, resources in resources_per_tz.items():
            res = result_per_tz[tz]
            res_intervals = Intervals(res)
            for resource in resources:
                if resource in per_resource_result:
                    resource_specific_result = [(max(bounds_per_tz[tz][0], tz.localize(val[0])), min(bounds_per_tz[tz][1], tz.localize(val[1])), val[2])
                        for val in per_resource_result[resource]]
                    result_per_resource_id[resource.id] = Intervals(itertools.chain(res, resource_specific_result))
                else:
                    result_per_resource_id[resource.id] = res_intervals
        return result_per_resource_id

    def _attendance_intervals_batch(self, start_dt, end_dt, resources=None, tz=None):
        res = super(ResourceCalendar, self)._attendance_intervals_batch(start_dt=start_dt, end_dt=end_dt, resources=resources, tz=tz)
        if self.env.context.get('from_leave_request',False) and not self.env.context.get('include_weekends',False):
            weekend = self._weekend_intervals(start_dt, end_dt, resources, tz)
            res.update(weekend)
        return res
