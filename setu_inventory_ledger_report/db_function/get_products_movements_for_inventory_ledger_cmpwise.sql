DROP FUNCTION if EXISTS public.si_ledger_get_products_movements_for_inventory_ledger_cmpwise(integer[], integer[], integer[], date, date);
CREATE OR REPLACE FUNCTION public.si_ledger_get_products_movements_for_inventory_ledger_cmpwise(
    IN company_ids integer[],
    IN product_ids integer[],
    IN category_ids integer[],
    IN start_date date,
    IN end_date date,
    IN wizard_id integer)
  --RETURNS TABLE(row_id bigint, company_id integer, company_name character varying, product_id integer, product_name character varying, product_category_id integer, category_name character varying, inventory_date date, opening_stock numeric, sales numeric, purchase numeric, sales_return numeric, purchase_return numeric, adjustment_in numeric, adjustment_out numeric, production_in numeric, production_out numeric, closing numeric) AS
  RETURNS void as
$BODY$
        DECLARE
            tr_start_date date;
            tr_end_date date;
            old_start_date date:= start_date;
            old_end_date date:= end_date;
            start_date timestamp without time zone := (start_date || ' 00:00:00')::timestamp without time zone;
            end_date timestamp without time zone:= (end_date || ' 23:59:59')::timestamp without time zone;

    BEGIN
        Drop Table if exists inventory_ledger_transaction_table;
        CREATE TEMPORARY TABLE inventory_ledger_transaction_table(
        row_id bigint,
            company_id integer,
            company_name character varying,
            product_id integer,
            product_name character varying,
            product_category_id integer,
            category_name character varying,
            inventory_date timestamp,
            opening_stock Numeric DEFAULT 0,
            sales Numeric DEFAULT 0,
            sales_return numeric DEFAULT 0,
            purchase Numeric DEFAULT 0,
            purchase_return numeric DEFAULT 0,
            adjustment_in Numeric DEFAULT 0,
            adjustment_out Numeric DEFAULT 0,
            production_in Numeric DEFAULT 0,
            production_out Numeric DEFAULT 0,
            closing Numeric DEFAULT 0
        );

    tr_start_date := '1900-01-01';
    tr_end_date := old_start_date - interval '1 day';

--    Insert into inventory_ledger_transaction_table(row_id, company_id, company_name, product_id, product_name, product_category_id, category_name, inventory_date,
--    opening_stock, sales, purchase, sales_return, purchase_return, adjustment_in, adjustment_out, production_in, production_out, closing)
    with row_datas as (
    Select
        row_number() over(partition by T1.product_id, T1.company_id order by T1.inventory_date::date, T1.product_id, T1.company_id) as row_id,
        T1.company_id, T1.company_name, T1.product_id, T1.product_name, T1.product_category_id, T1.category_name,
        T1.inventory_date::date, sum(T1.opening_stock) as opening_stock, sum(T1.sales) as sales,  sum(T1.purchase) as purchase,  sum(T1.sales_return) as sales_return, sum(T1.purchase_return) as purchase_return,
        sum(T1.adjustment_in) as adjustment_in, sum(T1.adjustment_out) as adjustment_out, sum(T1.production_in) as production_in, sum(T1.production_out) as production_out,
        sum(sum(T1.opening_stock) + sum(T1.purchase) - sum(T1.sales) + sum(T1.sales_return) - sum(T1.purchase_return) + sum(T1.adjustment_in) - sum(T1.adjustment_out) + sum(T1.production_in) - sum(T1.production_out))
        over(partition by T1.product_id, T1.company_id order by T1.inventory_date::date, T1.product_id, T1.company_id) as closing
    From  (

    Select
        move.company_id,
        cmp.name as company_name,
        move.product_id as product_id,
        prod.default_code as product_name,
        tmpl.categ_id as product_category_id,
        cat.complete_name as category_name,
        move.date as inventory_date,
        0 as opening_stock,
        case when source.usage = 'internal' and dest.usage = 'customer' then move.product_uom_qty else 0 end as sales,
        case when source.usage = 'customer' and dest.usage = 'internal' then move.product_uom_qty else 0 end as sales_return,
        case when source.usage = 'supplier' and dest.usage = 'internal' then move.product_uom_qty else 0 end as purchase,
        case when source.usage = 'internal' and dest.usage = 'supplier' then move.product_uom_qty else 0 end as purchase_return,
        case when source.usage = 'internal' and dest.usage = 'inventory' then move.product_uom_qty else 0 end as adjustment_out,
        case when source.usage = 'inventory' and dest.usage = 'internal' then move.product_uom_qty else 0 end as adjustment_in,
        case when source.usage = 'internal' and dest.usage = 'production' then move.product_uom_qty else 0 end as production_out,
        case when source.usage = 'production' and dest.usage = 'internal' then move.product_uom_qty else 0 end as production_in
    from stock_move move
        Inner Join stock_location source on source.id = move.location_id
        Inner Join stock_location dest on dest.id = move.location_dest_id
        Inner Join res_company cmp on cmp.id = move.company_id
        Inner Join product_product prod on prod.id = move.product_id
        Inner Join product_template tmpl on tmpl.id = prod.product_tmpl_id
        Inner Join product_category cat on cat.id = tmpl.categ_id

    Where prod.active = true and tmpl.active = true and
    move.state ='done' and move.date >= start_date and move.date <= end_date
    and not (source.usage = 'internal' and dest.usage='internal') and not (source.usage = 'transit' or dest.usage='transit')
    --company dynamic condition
    and 1 = case when array_length(company_ids,1) >= 1 then
        case when tmpl.company_id = ANY(company_ids) then 1 else 0 end
        else 1 end
    --product dynamic condition
    and 1 = case when array_length(product_ids,1) >= 1 then
        case when move.product_id = ANY(product_ids) then 1 else 0 end
        else 1 end
    --category dynamic condition
    and 1 = case when array_length(category_ids,1) >= 1 then
        case when tmpl.categ_id = ANY(category_ids) then 1 else 0 end
        else 1 end

    Union All

    select T.company_id, T.company_name, T.product_id, T.product_name, T.product_category_id, T.category_name, old_start_date as inventory_date, sum(T.opening_stock) as opening_stock,
    0,0,0,0,0,0,0,0
    from si_ledger_get_products_opening_stock(company_ids, product_ids, category_ids, '{}', tr_start_date, tr_end_date) T
    Group by T.company_id, T.company_name, T.product_id, T.product_name, T.product_category_id, T.category_name

    Union All

    -- Set default 0 value for each transaction for each products for each warehouse
     Select T2.company_id, T2.company_name, T2.product_id, T2.product_name, T2.product_category_id, T2.category_name, generate_series(start_date, end_date, '1 day'::interval)::date as inventory_date
    , 0 as opening_stock, 0,0,0,0,0,0,0,0
    From (
	Select cmp.id as company_id, cmp.name as company_name, prod.id as product_id, prod.default_code as product_name,  cat.id as product_category_id, cat.complete_name as category_name
	From
		product_product prod, product_template tmpl, product_category cat, res_company cmp
	where prod.product_tmpl_id = tmpl.id and tmpl.categ_id = cat.id
	and prod.active = true and tmpl.active = true
	--company dynamic condition
    and 1 = case when array_length(company_ids,1) >= 1 then
        case when tmpl.company_id = ANY(company_ids) then 1 else 0 end
        else 1 end
    --product dynamic condition
    and 1 = case when array_length(product_ids,1) >= 1 then
        case when prod.id = ANY(product_ids) then 1 else 0 end
        else 1 end
    --category dynamic condition
    and 1 = case when array_length(category_ids,1) >= 1 then
        case when cat.id = ANY(category_ids) then 1 else 0 end
        else 1 end
    )T2
    Group by T2.company_id, T2.company_name, T2.product_id, T2.product_name, T2.product_category_id, T2.category_name

    )T1
    Group by T1.company_id, T1.company_name, T1.product_id, T1.product_name, T1.product_category_id, T1.category_name, T1.inventory_date::date
    )



--    Return query
--    WITH RECURSIVE summary_cte(row_id, company_id, company_name, product_id, product_name, product_category_id, category_name, inventory_date,
--    opening_stock, sales, purchase, sales_return, purchase_return, adjustment_in, adjustment_out, production_in, production_out, closing)
--    AS (
--        Select
--            S1.row_id,
--            S1.company_id, S1.company_name, S1.product_id, S1.product_name, S1.product_category_id, S1.category_name,
--            S1.inventory_date::date, S1.opening_stock, S1.sales, S1.purchase, S1.sales_return, S1.purchase_return, S1.adjustment_in, S1.adjustment_out, S1.production_in, S1.production_out,
--            (S1.opening_stock + S1.purchase - S1.sales + S1.sales_return - S1.purchase_return + S1.adjustment_in -
--            S1.adjustment_out + S1.production_in - S1.production_out) as closing
--        from inventory_ledger_transaction_table S1
--        Where S1.row_id = 1
--
--            UNION ALL
--
--        SELECT summ.row_id,
--            summ.company_id, summ.company_name, summ.product_id, summ.product_name, summ.product_category_id, summ.category_name,
--            summ.inventory_date::date, (summ_cte.opening_stock + summ_cte.purchase - summ_cte.sales + summ_cte.sales_return - summ_cte.purchase_return + summ_cte.adjustment_in - summ_cte.adjustment_out + summ_cte.production_in - summ_cte.production_out
--            ), summ.sales, summ.purchase, summ.sales_return, summ.purchase_return, summ.adjustment_in, summ.adjustment_out, summ.production_in, summ.production_out,
--            ((summ_cte.opening_stock + summ_cte.purchase - summ_cte.sales + summ_cte.sales_return - summ_cte.purchase_return + summ_cte.adjustment_in - summ_cte.adjustment_out + summ_cte.production_in - summ_cte.production_out)
--            + summ.purchase - summ.sales + summ.sales_return - summ.purchase_return + summ.adjustment_in - summ.adjustment_out + summ.production_in - summ.production_out) as closing
--        FROM inventory_ledger_transaction_table summ, summary_cte summ_cte
--        WHERE summ.row_id - 1 = summ_cte.row_id and summ.product_id = summ_cte.product_id and summ.company_id = summ_cte.company_id
--    )
--
--    SELECT * FROM summary_cte order by 2,4,8;
Insert into setu_inventory_ledger_bi_report(company_id, product_id, product_category_id, inventory_date,
    opening_stock, sales, purchase, sales_return, purchase_return, adjustment_in, adjustment_out, production_in, production_out, closing, wizard_id)
select 
d.company_id, d.product_id, d.product_category_id, d.inventory_date,
    d.opening_stock, d.sales, d.purchase, d.sales_return, d.purchase_return, d.adjustment_in, d.adjustment_out, d.production_in, d.production_out, d.closing, wizard_id
from (
select
		line_one.company_id, line_one.product_id, line_one.product_category_id, line_one.inventory_date::date,
    line_one.opening_stock, line_one.sales, line_one.purchase, line_one.sales_return, line_one.purchase_return, line_one.adjustment_in, line_one.adjustment_out, line_one.production_in, line_one.production_out, line_one.closing
	from
		row_datas line_one where line_one.row_id = 1
UNION ALL
select
	 r2.company_id, r2.product_id, r2.product_category_id, r2.inventory_date::date,
    r1.closing as opening_stock, r2.sales, r2.purchase, r2.sales_return, r2.purchase_return, r2.adjustment_in, r2.adjustment_out, r2.production_in, r2.production_out, r2.closing
	from
		row_datas r1 join row_datas r2
		                            on r1.product_id = r2.product_id
									  and r1.company_id = r2.company_id
									  --and r1.warehouse_id = r2.warehouse_id
									  and r1.product_category_id = r2.product_category_id
									  and r1.row_id = r2.row_id-1
									  --where r1.closing != 0 or r2.closing != 0
	)d order by 1,2,4;

END; $BODY$
LANGUAGE plpgsql VOLATILE
COST 100;
--ROWS 1000;
