# scripts/add_mart_datasource.py
import great_expectations as gx


def main() -> None:
    context = gx.get_context()

    ds = context.sources.add_or_update_sql(
        name="mart_retail_postgres",
        connection_string="postgresql+psycopg2://dpuser:dppass@dp_postgres:5432/project_retail",
    )

    # Register mart assets across their schemas
    assets = [
        ("mart_dims", "dim_customer"),
        ("mart_dims", "dim_date"),
        ("mart_dims", "dim_stock"),
        ("mart_sales", "fct_sales"),
        ("mart_customer", "fct_customer_sales"),
    ]

    for schema_name, table_name in assets:
        ds.add_table_asset(name=table_name, table_name=table_name, schema_name=schema_name)

    print("Added mart assets: " + ", ".join(a[1] for a in assets))


if __name__ == "__main__":
    main()

