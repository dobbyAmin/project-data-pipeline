# scripts/add_core_datasources.py
import great_expectations as gx


def main() -> None:
    context = gx.get_context()

    ds = context.sources.add_or_update_sql(
        name="core_retail_postgres",
        connection_string="postgresql+psycopg2://dpuser:dppass@dp_postgres:5432/project_retail",
    )

    core_tables = [
        "customers",
        "sales",
        "stock",
        "date",
    ]

    for tbl in core_tables:
        ds.add_table_asset(name=tbl, table_name=tbl, schema_name="core")

    print("Added GX datasource and core assets: " + ", ".join(core_tables))


if __name__ == "__main__":
    main()

