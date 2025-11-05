# Products Data Cleaning Script
# ----------------------------
# Reads raw products data, cleans it, and saves prepared CSV.

import pandas as pd
import os

# -------------------------
# File paths
# -------------------------
RAW_FILE = os.path.abspath("data/raw/products_data.csv")
CLEAN_FILE = os.path.abspath("data/prepared/products_data_prepared.csv")

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
# Fill missing ProductName or Category with 'Unknown'
for col in ['ProductName', 'Category', 'ProductSupplierRegion']:
    if col not in df.columns:
        df[col] = 'Unknown'
    else:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            print(f"Found {missing_count} missing {col}. Filling with 'Unknown'.")
            df[col] = df[col].fillna('Unknown')

# Fill numeric columns with 0
for col in ['UnitPrice', 'ProductDiscountPercent']:
    if col not in df.columns:
        df[col] = 0.0
    else:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            print(f"Found {missing_count} missing {col}. Filling with 0.")
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

# -------------------------
# Step 3: Remove invalid / negative numbers
# -------------------------
for col in ['UnitPrice', 'ProductDiscountPercent']:
    before = len(df)
    df = df[df[col] >= 0]
    print(f"Removed {before - len(df)} rows with negative {col} values.")

# -------------------------
# Step 4: Ensure correct data types
# -------------------------
df['ProductID'] = df['ProductID'].astype(str)
for col in ['UnitPrice', 'ProductDiscountPercent']:
    df[col] = df[col].astype(float)

# -------------------------
# Save cleaned data
# -------------------------
df.to_csv(CLEAN_FILE, index=False)
print(f"Cleaned products data saved to {CLEAN_FILE}")
print(f"Final cleaned shape: {df.shape}")
