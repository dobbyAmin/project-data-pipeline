# scripts/create_expectation_suites.py
import great_expectations as gx

context = gx.get_context()

ds = context.datasources["raw_retail_postgres"]
asset = ds.get_asset("raw_data")

suite_name = "validate_raw_data"
suite = context.add_or_update_expectation_suite(suite_name)

validator_raw = context.get_validator(
    batch_request=asset.build_batch_request(),
    expectation_suite_name=suite_name,
)

validator_raw.expect_table_columns_to_match_ordered_list(
    column_list=["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]
)

validator_raw.expect_column_values_to_not_be_null("InvoiceNo")

# Quantity > 0 (mostly 95%)
validator_raw.expect_column_values_to_be_between(
    column="Quantity", min_value=0, strict_min=True, mostly=0.95,
    meta={"notes": "KPI: Invalid Quantity (< 0 <= 5%)"}
)

# UnitPrice > 0 (mostly 98%)
validator_raw.expect_column_values_to_be_between(
    column="UnitPrice", min_value=0, strict_min=True, mostly=0.98,
    meta={"notes": "KPI: Invalid UnitPrice (<= 0 <= 2%)"}
)

# UnitPrice > 0 (assert แบบเข้มงวด ไม่มี mostly)
validator_raw.expect_column_values_to_be_between(
    column="UnitPrice", min_value=0, strict_min=True,
    meta={"notes": "KPI: UnitPrice <= 0"}
)

validator_raw.expect_column_values_to_not_be_null(
    column="CustomerID",
    meta={"notes": "KPI: CustomerID must not be NULL"}
)

validator_raw.save_expectation_suite(discard_failed_expectations=False)
print(f"--- Suite '{suite_name}' created/updated ---")