# scripts/create_checkpoints.py
import great_expectations as gx

context = gx.get_context()

# 1. Checkpoint สำหรับ Raw Data (CSV)
context.add_or_update_checkpoint(
    name="raw_data_checkpoint",
    validations=[
        {
            "batch_request": {
                "datasource_name": "raw_retail_postgres",
                "data_asset_name": "raw_data"
            },
            "expectation_suite_name": "validate_raw_data",
        }
    ],
)
print("✅ Created checkpoint: raw_data_checkpoint")
