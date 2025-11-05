# Data Cleaning Script - Sales Table
# ----------------------------------
# Cleans raw sales data by:
# - Removing duplicates
# - Handling missing values
# - Ensuring correct data types
# - Removing outliers or invalid values
# - Logging all steps

import pandas as pd
import os

# -------------------------
# File paths
# -------------------------
RAW_FILE = os.path.abspath("data/raw/sales_data.csv")
CLEAN_FILE = os.path.abspath("data/prepared/sales_data_prepared.csv")

# Ensure prepared directory exists
os.makedirs(os.path.dirname(CLEAN_FILE), exist_ok=True)

# -------------------------
# Load raw data
# -------------------------
print(f"Loading raw data from {RAW_FILE}...")
df = pd.read_csv(RAW_FILE)
print(f"Raw data shape: {df.shape}")

# -------------------------
# Step 1: Remove duplicates
# -------------------------
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows.")

# -------------------------
# Step 2: Handle missing values
# -------------------------
# Fill missing CustomerID, ProductID, StoreID with 0
missing_ids = df[['CustomerID', 'ProductID', 'StoreID']].isna().sum().sum()
if missing_ids > 0:
    print(f"Found {missing_ids} missing ID values. Filling with 0.")
    df[['CustomerID', 'ProductID', 'StoreID']] = df[['CustomerID', 'ProductID', 'StoreID']].fillna(
        0
    )

# Parse SaleDate
df['SaleDate'] = pd.to_datetime(df['SaleDate'], errors='coerce')
invalid_dates = df['SaleDate'].isna().sum()
if invalid_dates > 0:
    print(f"Found {invalid_dates} invalid SaleDate values. Filling with today.")
    df['SaleDate'] = df['SaleDate'].fillna(pd.Timestamp.today())

# -------------------------
# Step 3: Remove outliers / invalid numbers
# -------------------------
# Convert numeric columns, coerce errors to NaN
df['SaleAmount'] = pd.to_numeric(df['SaleAmount'], errors='coerce')
df['DiscountPercent'] = pd.to_numeric(df['DiscountPercent'], errors='coerce')

# Remove rows with invalid SaleAmount or DiscountPercent
before = len(df)
df = df[(df['SaleAmount'] >= 0) & (df['DiscountPercent'].between(0, 100))]
print(f"Removed {before - len(df)} rows with invalid SaleAmount or DiscountPercent.")

# -------------------------
# Step 4: Standardize payment type
# -------------------------
valid_payment_types = ['DebitCard', 'CreditCard', 'Cash', 'GiftCard']
invalid_payment_count = (~df['SalePaymentType'].isin(valid_payment_types)).sum()
if invalid_payment_count > 0:
    print(f"Found {invalid_payment_count} invalid payment types. Setting to 'Other'.")
    df.loc[~df['SalePaymentType'].isin(valid_payment_types), 'SalePaymentType'] = 'Other'

# -------------------------
# Step 5: Ensure correct data types
# -------------------------
df['TransactionID'] = df['TransactionID'].astype(str)
df['CustomerID'] = df['CustomerID'].astype(str)
df['ProductID'] = df['ProductID'].astype(str)
df['StoreID'] = df['StoreID'].astype(str)
df['CampaignID'] = df['CampaignID'].fillna(0).astype(int)
df['SaleAmount'] = df['SaleAmount'].astype(float)
df['DiscountPercent'] = df['DiscountPercent'].astype(float)

# -------------------------
# Save cleaned data
# -------------------------
df.to_csv(CLEAN_FILE, index=False)
print(f"Cleaned sales data saved to {CLEAN_FILE}")
print(f"Final cleaned shape: {df.shape}")
