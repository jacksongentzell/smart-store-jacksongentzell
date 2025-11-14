"""ETL Script to Load Data into the Data Warehouse
This script extracts cleaned data from prepared CSV files, transforms it as necessary,
and loads it into a SQLite data warehouse."""

"""
etl_to_dw.py
Robust ETL to create a small DW from your cleaned CSVs found in data/clean/.

Usage (from project root):
    python -m analytics_project.etl_to_dw
"""

import sqlite3
import pandas as pd
from pathlib import Path
import os

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(r"C:\Repos\smart-store-jacksongentzell")
DATA_DIR = PROJECT_ROOT / "data"
CLEAN_DIR = DATA_DIR / "clean"
DW_DIR = DATA_DIR / "dw"
DB_PATH = DW_DIR / "smart_store_dw.db"

# Ensure DW directory exists
os.makedirs(DW_DIR, exist_ok=True)

# CSV files
CUSTOMERS_CSV = CLEAN_DIR / "customers_cleaned.csv"
PRODUCTS_CSV = CLEAN_DIR / "products_cleaned.csv"
SALES_CSV = CLEAN_DIR / "sales_cleaned.csv"


# -----------------------------
# Helper Functions
# -----------------------------
def clean_numeric_column(df, col):
    """Clean numeric columns: remove %, convert to float, handle errors."""
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace("%", "", regex=False).str.strip(), errors="coerce"
        )
    return df


# -----------------------------
# ETL Functions
# -----------------------------
def create_schema(cursor: sqlite3.Cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        region TEXT,
        join_date TEXT,
        reward_points INTEGER,
        status TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        unit_price REAL,
        product_discount_percent REAL,
        supplier_region TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        transaction_id INTEGER PRIMARY KEY,
        sale_date TEXT,
        customer_id INTEGER,
        product_id INTEGER,
        store_id INTEGER,
        campaign_id INTEGER,
        sale_amount REAL,
        discount_percent REAL,
        sale_payment_type TEXT
    );
    """)


def insert_customers(df: pd.DataFrame, cursor: sqlite3.Cursor):
    df = df.rename(
        columns={
            "CustomerID": "customer_id",
            "Name": "name",
            "Region": "region",
            "JoinDate": "join_date",
            "CustomerRewardPoints": "reward_points",
            "CustomerStatus": "status",
        }
    )
    df = df.drop_duplicates(subset=["customer_id"])
    df["reward_points"] = pd.to_numeric(df["reward_points"], errors="coerce")
    df = df.dropna(subset=["customer_id"])
    df["customer_id"] = df["customer_id"].astype(int)
    df.to_sql("customer", cursor.connection, if_exists="append", index=False)


def insert_products(df: pd.DataFrame, cursor: sqlite3.Cursor):
    df = df.rename(
        columns={
            "ProductID": "product_id",
            "ProductName": "product_name",
            "Category": "category",
            "UnitPrice": "unit_price",
            "ProductDiscountPercent": "product_discount_percent",
            "ProductSupplierRegion": "supplier_region",
        }
    )
    df = df.drop_duplicates(subset=["product_id"])

    df = clean_numeric_column(df, "product_id")
    df = clean_numeric_column(df, "unit_price")
    df = clean_numeric_column(df, "product_discount_percent")

    df = df.dropna(subset=["product_id", "unit_price", "product_discount_percent"])
    df["product_id"] = df["product_id"].astype(int)

    df.to_sql("product", cursor.connection, if_exists="append", index=False)


def insert_sales(df: pd.DataFrame, cursor: sqlite3.Cursor):
    df = df.rename(
        columns={
            "TransactionID": "transaction_id",
            "SaleDate": "sale_date",
            "CustomerID": "customer_id",
            "ProductID": "product_id",
            "StoreID": "store_id",
            "CampaignID": "campaign_id",
            "SaleAmount": "sale_amount",
            "DiscountPercent": "discount_percent",
            "SalePaymentType": "sale_payment_type",
        }
    )

    # Clean numeric columns
    for col in [
        "transaction_id",
        "customer_id",
        "product_id",
        "store_id",
        "campaign_id",
        "sale_amount",
        "discount_percent",
    ]:
        df = clean_numeric_column(df, col)

    # Drop rows with missing critical numeric values
    df = df.dropna(subset=["transaction_id", "customer_id", "product_id", "sale_amount"])

    # Drop duplicate transaction_id
    df = df.drop_duplicates(subset=["transaction_id"])

    # Ensure integer types for IDs
    df["transaction_id"] = df["transaction_id"].astype(int)
    df["customer_id"] = df["customer_id"].astype(int)
    df["product_id"] = df["product_id"].astype(int)

    df.to_sql("sales", cursor.connection, if_exists="append", index=False)


# -----------------------------
# Main ETL
# -----------------------------
def main():
    print("Connecting to SQLite database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Creating schema...")
    create_schema(cursor)

    print("Deleting existing records...")
    cursor.execute("DELETE FROM sales;")
    cursor.execute("DELETE FROM product;")
    cursor.execute("DELETE FROM customer;")
    conn.commit()

    print("Loading CSVs...")
    customers_df = pd.read_csv(CUSTOMERS_CSV)
    products_df = pd.read_csv(PRODUCTS_CSV)
    sales_df = pd.read_csv(SALES_CSV)

    print("Inserting customers...")
    insert_customers(customers_df, cursor)

    print("Inserting products...")
    insert_products(products_df, cursor)

    print("Inserting sales...")
    insert_sales(sales_df, cursor)

    conn.commit()

    # Validation
    cursor.execute("SELECT COUNT(*) FROM customer;")
    print(f"Customers loaded: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM product;")
    print(f"Products loaded: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM sales;")
    print(f"Sales loaded: {cursor.fetchone()[0]}")

    conn.close()
    print("ETL completed successfully!")


if __name__ == "__main__":
    main()
