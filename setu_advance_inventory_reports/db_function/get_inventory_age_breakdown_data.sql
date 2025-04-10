DROP FUNCTION if exists get_inventory_age_breakdown_data(integer[],integer[],integer[],integer);
CREATE OR REPLACE FUNCTION public.get_inventory_age_breakdown_data(
    IN company_ids integer[],
    IN product_ids integer[],
    IN category_ids integer[],
    IN breakdown_days integer
)
RETURNS TABLE(
    company_id integer, company_name character varying, product_id integer, product_name character varying,
    product_category_id integer, category_name character varying, total_stock numeric, total_stock_value numeric,
    breakdown1_qty numeric, breckdown1_value numeric,
    breakdown2_qty numeric, breckdown2_value numeric, breakdown3_qty numeric, breckdown3_value numeric,
    breakdown4_qty numeric, breckdown4_value numeric, breakdown5_qty numeric, breckdown5_value numeric,
    breakdown6_qty numeric, breckdown6_value numeric, breakdown7_qty numeric, breckdown7_value numeric
) as
$BODY$
    BEGIN
        Return Query
        Select
            GD.company_id, GD.company_name, GD.product_id, GD.product_code, GD.category_id, GD.category_name,
            sum(stock_qty) as "total_stock", sum(stock_value) as "total_stock_value",
            sum(GD.breakdown1_qty) as "breakdown1_qty", sum(GD.breakdown1_value) as "breakdown1_value",
            sum(GD.breakdown2_qty) as "breakdown2_qty", sum(GD.breakdown2_value) as "breakdown2_value",
            sum(GD.breakdown3_qty) as "breakdown3_qty", sum(GD.breakdown3_value) as "breakdown3_value",
            sum(GD.breakdown4_qty) as "breakdown4_qty", sum(GD.breakdown4_value) as "breakdown4_value",
            sum(GD.breakdown5_qty) as "breakdown5_qty", sum(GD.breakdown5_value) as "breakdown5_value",
            sum(GD.breakdown6_qty) as "breakdown6_qty", sum(GD.breakdown6_value) as "breakdown6_value",
            sum(GD.breakdown7_qty) as "breakdown7_qty", sum(GD.breakdown7_value) as "breakdown7_value"
        From (
        Select
            T.company_id,
            T.company_name,
            T.product_id,
            T.product_code,
            T.category_id,
            T.category_name,
            stock_qty,
            stock_value,
            case when stock_age <= breakdown_days then stock_qty else 0 end as "breakdown1_qty",
            case when stock_age <= breakdown_days then stock_value else 0 end as "breakdown1_value",

            case when stock_age > breakdown_days and stock_age <= (breakdown_days * 2) then stock_qty else 0 end as "breakdown2_qty",
            case when stock_age > breakdown_days and stock_age <= (breakdown_days * 2) then stock_value else 0 end as "breakdown2_value",

            case when stock_age > (breakdown_days * 2) and stock_age <= (breakdown_days * 3) then stock_qty else 0 end as "breakdown3_qty",
            case when stock_age > (breakdown_days * 2) and stock_age <= (breakdown_days * 3) then stock_value else 0 end as "breakdown3_value",

            case when stock_age > (breakdown_days * 3) and stock_age <= (breakdown_days * 4) then stock_qty else 0 end as "breakdown4_qty",
            case when stock_age > (breakdown_days * 3) and stock_age <= (breakdown_days * 4) then stock_value else 0 end as "breakdown4_value",

            case when stock_age > (breakdown_days * 4) and stock_age <= (breakdown_days * 5) then stock_qty else 0 end as "breakdown5_qty",
            case when stock_age > (breakdown_days * 4) and stock_age <= (breakdown_days * 5) then stock_value else 0 end as "breakdown5_value",

            case when stock_age > (breakdown_days * 5) and stock_age <= (breakdown_days * 6) then stock_qty else 0 end as "breakdown6_qty",
            case when stock_age > (breakdown_days * 5) and stock_age <= (breakdown_days * 6) then stock_value else 0 end as "breakdown6_value",

            case when stock_age > (breakdown_days * 6) then stock_qty else 0 end as "breakdown7_qty",
            case when stock_age > (breakdown_days * 6) then stock_value else 0 end as "breakdown7_value"

        from
        (   select
                row_number() over(partition by all_d.company_id, all_d.product_id order by all_d.company_id, all_d.product_id, all_d.move_date) row_id,
                all_d.company_id,
                all_d.company_name,
                all_d.stock_age,
                all_d.product_id,
                all_d.product_code,
                all_d.category_id,
                all_d.category_name,
                sum(all_d.stock_qty) as stock_qty,
                sum(all_d.stock_value) as stock_value
            from (
            Select
                layer.company_id,
                cmp.name as company_name,
                case when move.date is null then (now()::date - layer.create_date::date) else (now()::date - move.date::date) end as stock_age,
                move.date::date as move_date,
                layer.product_id,
--                prod.default_code as product_code,
--                case when prod.default_code is not null then
                concat('['||(prod.default_code||'')||']'||' '||(tmpl.name ->>'en_US'))::character varying as product_code,
                --coalesce(prod.default_code, tmpl.name) as product_code,
                --prod.default_code as product_code,
                tmpl.categ_id as category_id,
                cat.complete_name as category_name,
                sum(layer.remaining_qty) stock_qty,
                sum(layer.remaining_value) stock_value
            from
                stock_valuation_layer layer
                    left Join stock_move move on move.id = layer.stock_move_id
                    left Join product_product prod on prod.id = layer.product_id
                    left Join product_template tmpl on tmpl.id = prod.product_tmpl_id
                    left Join product_category cat on cat.id = tmpl.categ_id
                    left Join res_company cmp on cmp.id = layer.company_id
                    left Join ir_property on  ir_property.res_id = 'product.category,' || tmpl.categ_id
                    and ir_property.company_id = layer.company_id
                    and ir_property.name = 'property_cost_method'
                    and ir_property.value_text not in ('standard')
            Where remaining_qty > 0 and prod.active = True and tmpl.active = True and --and layer.product_id = 284
            1 = case when array_length(product_ids,1) >= 1 then
                case when layer.product_id = ANY(product_ids) then 1 else 0 end
                else 1 end
            and 1 = case when array_length(category_ids,1) >= 1 then
                case when tmpl.categ_id = ANY(category_ids) then 1 else 0 end
                else 1 end
            and 1 = case when array_length(company_ids,1) >= 1 then
                case when layer.company_id = ANY(company_ids) then 1 else 0 end
                else 1 end
            group by layer.company_id, cmp.name, move.date, layer.create_date, layer.product_id, prod.default_code, tmpl.name, tmpl.categ_id, cat.complete_name

            UNION ALL

            Select
                layer.company_id,
                cmp.name as company_name,
                (now()::date - move.date::date) stock_age,
                move.date::date as move_date,
                layer.product_id,
                concat('['||(prod.default_code||'')||']'||' '||(tmpl.name ->>'en_US'))::character varying as product_code,                --coalesce(prod.default_code, tmpl.name) as product_code,
                --prod.default_code as product_code,
                tmpl.categ_id as category_id,
                cat.complete_name as category_name,
                sum(layer.quantity) stock_qty,
                sum(layer.value) stock_value
            from
                stock_valuation_layer layer
                    Inner Join stock_move move on move.id = layer.stock_move_id
                    Inner Join product_product prod on prod.id = layer.product_id
                    Inner Join product_template tmpl on tmpl.id = prod.product_tmpl_id
                    Inner Join product_category cat on cat.id = tmpl.categ_id
                    Inner Join res_company cmp on cmp.id = layer.company_id
                    Inner Join ir_property on  ir_property.res_id = 'product.category,' || tmpl.categ_id
                    and ir_property.company_id = layer.company_id
                and ir_property.name = 'property_cost_method'
                and ir_property.value_text not in ('fifo','average')
                Where (remaining_qty is null)
                and 1 = case when array_length(product_ids,1) >= 1 then
                    case when layer.product_id = ANY(product_ids) then 1 else 0 end
                    else 1 end
                and 1 = case when array_length(category_ids,1) >= 1 then
                    case when tmpl.categ_id = ANY(category_ids) then 1 else 0 end
                    else 1 end
                and 1 = case when array_length(company_ids,1) >= 1 then
                    case when layer.company_id = ANY(company_ids) then 1 else 0 end
                    else 1 end
                and prod.active = True and tmpl.active = True
                group by layer.company_id, cmp.name, move.date, layer.product_id, prod.default_code, tmpl.name, tmpl.categ_id, cat.complete_name

        UNION ALL

                Select
                    layer.company_id as company_id,
                    cmp.name as company_name,
                    (now()::date - layer.create_date::date) stock_age,
                    layer.create_date as move_date,
                    layer.product_id as product_id,
                    concat('['||(prod.default_code||'')||']'||' '||(tmpl.name ->>'en_US'))::character varying as product_code,
                    --coalesce(prod.default_code, tmpl.name) as product_code,

                    tmpl.categ_id as category_id,
                    cat.complete_name as category_name,

                    sum(layer.quantity) as stock_qty,
                    sum(layer.value) stock_value

                from
                    stock_valuation_layer layer
                        --Inner Join stock_move move on move.id = layer.stock_move_id
                        Inner Join product_product prod on prod.id = layer.product_id
                        Inner Join product_template tmpl on tmpl.id = prod.product_tmpl_id
                        Inner Join product_category cat on cat.id = tmpl.categ_id
                        Inner Join res_company cmp on cmp.id = layer.company_id
                        Inner Join ir_property on  ir_property.res_id = 'product.category,' || tmpl.categ_id
                        and ir_property.company_id = layer.company_id
                    and ir_property.name = 'property_cost_method'
                    and ir_property.value_text not in ('fifo','average')
                    Where (remaining_qty is null and layer.description ilike '%Product value manually modified%')
                    and 1 = case when array_length(product_ids,1) >= 1 then
                        case when layer.product_id = ANY(product_ids) then 1 else 0 end
                        else 1 end
                    and 1 = case when array_length(category_ids,1) >= 1 then
                        case when tmpl.categ_id = ANY(category_ids) then 1 else 0 end
                        else 1 end
                    and 1 = case when array_length(company_ids,1) >= 1 then
                        case when layer.company_id = ANY(company_ids) then 1 else 0 end
                        else 1 end
                    and prod.active = True and tmpl.active = True
                    group by layer.company_id, cmp.name, layer.create_date, layer.product_id, prod.default_code, tmpl.name, tmpl.categ_id, cat.complete_name
            )all_d
            group by all_d.company_id, all_d.company_name, all_d.stock_age, all_d.move_date, all_d.product_id, all_d.product_code, all_d.category_id, all_d.category_name
        )T
        )GD
        Group by GD.company_id, GD.company_name, GD.product_id, GD.product_code, GD.category_id, GD.category_name;
    END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100
ROWS 1000;
