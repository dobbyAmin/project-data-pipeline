# scripts/create_core_expectation_suites.py
import great_expectations as gx


def main() -> None:
    context = gx.get_context()

    ds = context.datasources["core_retail_postgres"]

    # customers suite
    suite_cust = context.add_or_update_expectation_suite("validate_core_customers")
    validator_cust = context.get_validator(
        batch_request=ds.get_asset("customers").build_batch_request(),
        expectation_suite_name=suite_cust.expectation_suite_name,
    )
    validator_cust.expect_table_columns_to_match_ordered_list(
        column_list=["customer_id", "country"]
    )
    validator_cust.expect_column_values_to_not_be_null("customer_id")
    validator_cust.save_expectation_suite(discard_failed_expectations=False)

    # sales suite
    suite_sales = context.add_or_update_expectation_suite("validate_core_sales")
    validator_sales = context.get_validator(
        batch_request=ds.get_asset("sales").build_batch_request(),
        expectation_suite_name=suite_sales.expectation_suite_name,
    )
    validator_sales.expect_table_columns_to_match_ordered_list(
        column_list=["invoice_no", 'stock_code', "customer_id", "quantity", "invoice_date"]
    )
    validator_sales.expect_column_values_to_not_be_null("invoice_no")
    validator_sales.expect_column_values_to_not_be_null("customer_id")
    validator_sales.expect_column_values_to_be_between(
        column="quantity", min_value=0, strict_min=True
    )
    validator_sales.expect_column_values_to_not_be_null("invoice_date")
    validator_sales.save_expectation_suite(discard_failed_expectations=False)

    # stock suite
    suite_stock = context.add_or_update_expectation_suite("validate_core_stock")
    validator_stock = context.get_validator(
        batch_request=ds.get_asset("stock").build_batch_request(),
        expectation_suite_name=suite_stock.expectation_suite_name,
    )
    validator_stock.expect_table_columns_to_match_ordered_list(
        column_list=["stock_code", "description", "unit_price"]
    )
    validator_stock.expect_column_values_to_not_be_null("stock_code")
    validator_stock.expect_column_values_to_be_between(
        column="unit_price", min_value=0, strict_min=True
    )
    validator_stock.save_expectation_suite(discard_failed_expectations=False)

    # date suite
    suite_date = context.add_or_update_expectation_suite("validate_core_date")
    validator_date = context.get_validator(
        batch_request=ds.get_asset("date").build_batch_request(),
        expectation_suite_name=suite_date.expectation_suite_name,
    )
    validator_date.expect_table_columns_to_match_ordered_list(
        column_list=["date_day", "day", "month", "year"]
    )
    validator_date.expect_column_values_to_be_between(
        column="day", min_value=1, max_value=31
    )
    validator_date.expect_column_values_to_be_between(
        column="month", min_value=1, max_value=12
    )
    validator_date.expect_column_values_to_not_be_null("year")
    validator_date.save_expectation_suite(discard_failed_expectations=False)

    print("Created/updated core expectation suites: customers, sales, stock, date")


if __name__ == "__main__":
    main()

