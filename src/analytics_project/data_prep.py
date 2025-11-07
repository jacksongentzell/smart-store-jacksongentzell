# Module 2: Initial Script to Verify Project Setup.

# File: src/analytics_project/data_prep.py.


# Imports after the opening docstring

import pathlib
import pandas as pd

# Absolute imports instead of relative
from src.utils.logger import init_logger, logger, project_root
from src.analytics_project.data_scrubber import DataScrubber

# Set up paths as constants
DATA_DIR: pathlib.Path = project_root.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")


# Define a reusable function that accepts a full path.
def read_and_log(path: pathlib.Path) -> pd.DataFrame:
    """Read a CSV at the given path into a DataFrame, with friendly logging."""
    try:
        logger.info(f"Reading raw data from {path}.")
        df = pd.read_csv(path)
        logger.info(
            f"{path.name}: loaded DataFrame with shape {df.shape[0]} rows x {df.shape[1]} cols"
        )
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error reading {path}: {e}")
        return pd.DataFrame()


def main() -> None:
    """Process raw data and clean it using DataScrubber."""
    logger.info("Starting data preparation...")

    # Build explicit paths for each file under data/raw
    customer_path = RAW_DATA_DIR.joinpath("customers_data.csv")
    product_path = RAW_DATA_DIR.joinpath("products_data.csv")
    sales_path = RAW_DATA_DIR.joinpath("sales_data.csv")

    # Prepare output folder
    prepared_dir = DATA_DIR.joinpath("prepared")
    prepared_dir.mkdir(parents=True, exist_ok=True)

    # ----------------------------
    # Process Customers
    # ----------------------------
    df_customers = read_and_log(customer_path)
    scrubber = DataScrubber(df_customers)
    scrubber.handle_missing_data(fill_value="Unknown").remove_duplicate_records()
    for col in scrubber.get_df().select_dtypes(include='object').columns:
        scrubber.format_column_strings_to_lower_and_trim(col)
    # Only rename columns that exist
    existing_rename = {
        k: v
        for k, v in {'cust_id': 'CustomerID', 'customer_name': 'CustomerName'}.items()
        if k in scrubber.get_df().columns
    }
    if existing_rename:
        scrubber.rename_columns(existing_rename)
    scrubber.get_df().to_csv(prepared_dir.joinpath("customers_cleaned.csv"), index=False)
    logger.info("Saved cleaned customers data.")

    # ----------------------------
    # Process Products
    # ----------------------------
    df_products = read_and_log(product_path)
    scrubber = DataScrubber(df_products)
    scrubber.handle_missing_data(fill_value="Unknown").remove_duplicate_records()
    for col in scrubber.get_df().select_dtypes(include='object').columns:
        scrubber.format_column_strings_to_lower_and_trim(col)
    scrubber.get_df().to_csv(prepared_dir.joinpath("products_cleaned.csv"), index=False)
    logger.info("Saved cleaned products data.")

    # ----------------------------
    # Process Sales
    # ----------------------------
    df_sales = read_and_log(sales_path)
    scrubber = DataScrubber(df_sales)
    scrubber.handle_missing_data(fill_value="Unknown").remove_duplicate_records()
    for col in scrubber.get_df().select_dtypes(include='object').columns:
        scrubber.format_column_strings_to_lower_and_trim(col)
    if 'sale_date' in scrubber.get_df().columns:
        scrubber.parse_dates_to_add_standard_datetime('sale_date')
    scrubber.get_df().to_csv(prepared_dir.joinpath("sales_cleaned.csv"), index=False)
    logger.info("Saved cleaned sales data.")

    logger.info("Data preparation complete.")


if __name__ == "__main__":
    # Initialize logger
    init_logger()
    main()
