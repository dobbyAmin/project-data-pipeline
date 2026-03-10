# scripts/create_mart_expectation_suites.py
import great_expectations as gx


def main() -> None:
    context = gx.get_context()
    ds = context.datasources["mart_retail_postgres"]

    # =============== Facts ===============
    # fct_sales
    suite_sales = context.add_or_update_expectation_suite("validate_mart_fct_sales")
    validator_sales = context.get_validator(
        batch_request=ds.get_asset("fct_sales").build_batch_request(),
        expectation_suite_name=suite_sales.expectation_suite_name,
    )
    validator_sales.expect_table_columns_to_match_ordered_list(
        column_list=["invoice_no", "invoice_date_key", "customer_key", "stock_key", "quantity"]
    )
    validator_sales.expect_column_values_to_not_be_null("invoice_no")
    validator_sales.expect_column_values_to_not_be_null("stock_key")
    validator_sales.expect_column_values_to_not_be_null("customer_key")
    validator_sales.expect_column_values_to_be_between(
        column="quantity", min_value=0, strict_min=True
    )
    validator_sales.expect_column_values_to_not_be_null("invoice_date_key")
    validator_sales.save_expectation_suite(discard_failed_expectations=False)

    # fct_customer_sales
    suite_cust = context.add_or_update_expectation_suite("validate_mart_fct_customer_sales")
    validator_cust = context.get_validator(
        batch_request=ds.get_asset("fct_customer_sales").build_batch_request(),
        expectation_suite_name=suite_cust.expectation_suite_name,
    )
    validator_cust.expect_table_columns_to_match_ordered_list(
        column_list=[
            "customer_key",
            "first_invoice_date_key",
            "last_invoice_date_key",
            "total_invoices",
            "total_quantity",
        ]
    )
    validator_cust.expect_column_values_to_not_be_null("customer_key")
    validator_cust.save_expectation_suite(discard_failed_expectations=False)

    # =============== Dims (basic checks) ===============
    # dim_customer
    suite_dim_customer = context.add_or_update_expectation_suite("validate_mart_dim_customer")
    v_dc = context.get_validator(
        batch_request=ds.get_asset("dim_customer").build_batch_request(),
        expectation_suite_name=suite_dim_customer.expectation_suite_name,
    )
    v_dc.expect_column_values_to_not_be_null("customer_key")
    v_dc.expect_column_values_to_be_unique("customer_key")
    v_dc.save_expectation_suite(discard_failed_expectations=False)

    # dim_date
    suite_dim_date = context.add_or_update_expectation_suite("validate_mart_dim_date")
    v_dd = context.get_validator(
        batch_request=ds.get_asset("dim_date").build_batch_request(),
        expectation_suite_name=suite_dim_date.expectation_suite_name,
    )
    v_dd.expect_column_values_to_not_be_null("date_key")
    v_dd.expect_column_values_to_be_unique("date_key")
    v_dd.save_expectation_suite(discard_failed_expectations=False)

    # dim_stock
    suite_dim_stock = context.add_or_update_expectation_suite("validate_mart_dim_stock")
    v_ds = context.get_validator(
        batch_request=ds.get_asset("dim_stock").build_batch_request(),
        expectation_suite_name=suite_dim_stock.expectation_suite_name,
    )
    v_ds.expect_column_values_to_not_be_null("stock_key")
    v_ds.expect_column_values_to_be_unique("stock_key")
    v_ds.save_expectation_suite(discard_failed_expectations=False)

    print("Created/updated mart suites: facts (sales, customer) + dims")


if __name__ == "__main__":
    main()

