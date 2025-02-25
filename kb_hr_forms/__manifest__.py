{
    'name': 'Customise HR Reports',
    'version': '14.0.0',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'HR',
    'summary': 'Customise HR Reports',
    'description': """Customise HR Reports""",
    'depends': [
            'hr',
            'hr_contract',
            'hr_fleet',
            'ohrms_loan'
               ],
    'data': [
        'security/ir.model.access.csv',
        'report/employment_contract.xml',
        'report/medical_insurance_request.xml',
        'report/final_settlement.xml',
        'report/resignation_form.xml',
        'report/disclaimer_argeement.xml',
        'report/receipt_car.xml',
        'report/effective_date_notice.xml',
        'report/clearance_form.xml',
        'report/receive_advance_deduct_salary.xml',
        'report/flight_ticket_request.xml',
        'report/residence_delivery.xml',
        'report/leave_application_form.xml',
        'report/non-renewal_of_residence.xml',
        'report/final_exit_visa.xml',
        'report/extension_of_exit_and_return_visa.xml',
        'report/renewal_of_residence.xml',
        'report/request_for_resignation.xml',
        'report/cancellation_of_final_exit_visa.xml',
        'report/job_offer.xml',
        'data/data.xml',
        'views/hr_employee_view.xml', 
        # 'views/id_card.xml',

        
        
    ],
}
