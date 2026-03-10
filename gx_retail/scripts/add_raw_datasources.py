# scripts/add_datasources.py
import great_expectations as gx

context = gx.get_context()

ds = context.sources.add_or_update_sql(
    name="raw_retail_postgres",
    connection_string="postgresql+psycopg2://dpuser:dppass@dp_postgres:5432/project_retail"
)

# 2.2 Assets (ตาราง) ที่ dbt สร้าง
ds.add_table_asset(
    name="raw_data",
    table_name="raw_data",
    schema_name="staging"
)

print("✅ Datasources and Assets added successfully.")