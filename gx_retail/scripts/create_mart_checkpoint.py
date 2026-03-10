# scripts/create_mart_checkpoint.py
import great_expectations as gx


def main() -> None:
    context = gx.get_context()
    ds = context.datasources["mart_retail_postgres"]

    # Checkpoint for sales mart
    context.add_or_update_checkpoint(
        name="mart_sales_checkpoint",
        validations=[
            {
                "batch_request": ds.get_asset("fct_sales").build_batch_request(),
                "expectation_suite_name": "validate_mart_fct_sales",
            }
        ],
    )

    # Checkpoint for customer mart
    context.add_or_update_checkpoint(
        name="mart_customer_checkpoint",
        validations=[
            {
                "batch_request": ds.get_asset("fct_customer_sales").build_batch_request(),
                "expectation_suite_name": "validate_mart_fct_customer_sales",
            }
        ],
    )

    print("Created/updated checkpoints: mart_sales_checkpoint, mart_customer_checkpoint")


if __name__ == "__main__":
    main()

