# scripts/create_core_checkpoint.py
import great_expectations as gx


def main() -> None:
    context = gx.get_context()
    ds = context.datasources["core_retail_postgres"]

    validations = [
        {
            "batch_request": ds.get_asset("customers").build_batch_request(),
            "expectation_suite_name": "validate_core_customers",
        },
        {
            "batch_request": ds.get_asset("sales").build_batch_request(),
            "expectation_suite_name": "validate_core_sales",
        },
        {
            "batch_request": ds.get_asset("stock").build_batch_request(),
            "expectation_suite_name": "validate_core_stock",
        },
        {
            "batch_request": ds.get_asset("date").build_batch_request(),
            "expectation_suite_name": "validate_core_date",
        },
    ]

    context.add_or_update_checkpoint(
        name="core_checkpoint",
        validations=validations,
    )

    print("Created/updated checkpoint: core_checkpoint")


if __name__ == "__main__":
    main()

