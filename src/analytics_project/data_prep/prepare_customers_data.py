# Data Cleaning Script - Customers Table
# -------------------------------------
# Cleans raw customers data by:
# - Removing duplicates
# - Handling missing values
# - Ensuring correct data types
# - Removing outliers or invalid values
# - Logging all steps

import pandas as pd
import os
from datetime import datetime

# -------------------------
# File paths
# -------------------------
RAW_FILE = os.path.abspath("data/raw/customers_data.csv")
CLEAN_FILE = os.path.abspath("data/prepared/customers_data_prepared.csv")

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
# Fill missing Name with 'Unknown Customer'
if 'Name' not in df.columns:
    df['Name'] = 'Unknown Customer'
else:
    missing_names = df['Name'].isna().sum()
    if missing_names > 0:
        print(f"Found {missing_names} missing Name. Filling with 'Unknown Customer'.")
        df['Name'] = df['Name'].fillna('Unknown Customer')

# Fill missing Region with 'Unknown'
if 'Region' not in df.columns:
    df['Region'] = 'Unknown'
else:
    missing_regions = df['Region'].isna().sum()
    if missing_regions > 0:
        print(f"Found {missing_regions} missing Region. Filling with 'Unknown'.")
        df['Region'] = df['Region'].fillna('Unknown')

# Handle JoinDate
if 'JoinDate' not in df.columns:
    df['JoinDate'] = pd.Timestamp.today()
else:
    df['JoinDate'] = pd.to_datetime(df['JoinDate'], errors='coerce')
    invalid_dates = df['JoinDate'].isna().sum()
    if invalid_dates > 0:
        print(f"Found {invalid_dates} invalid JoinDate values. Filling with today.")
        df['JoinDate'] = df['JoinDate'].fillna(pd.Timestamp.today())

# Fill missing numeric columns
for col in ['CustomerRewardPoints']:
    if col not in df.columns:
        df[col] = 0
    else:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            print(f"Found {missing_count} missing {col}. Filling with 0.")
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Fill missing CustomerStatus with 'New'
if 'CustomerStatus' not in df.columns:
    df['CustomerStatus'] = 'New'
else:
    missing_status = df['CustomerStatus'].isna().sum()
    if missing_status > 0:
        print(f"Found {missing_status} missing CustomerStatus. Filling with 'New'.")
        df['CustomerStatus'] = df['CustomerStatus'].fillna('New')

# -------------------------
# Step 3: Remove invalid values
# -------------------------
# Ensure RewardPoints are non-negative
before = len(df)
df = df[df['CustomerRewardPoints'] >= 0]
print(f"Removed {before - len(df)} rows with negative CustomerRewardPoints.")

# -------------------------
# Step 4: Ensure correct data types
# -------------------------
df['CustomerID'] = df['CustomerID'].astype(str)
df['CustomerRewardPoints'] = df['CustomerRewardPoints'].astype(int)
df['JoinDate'] = pd.to_datetime(df['JoinDate'])
df['Name'] = df['Name'].astype(str)
df['Region'] = df['Region'].astype(str)
df['CustomerStatus'] = df['CustomerStatus'].astype(str)

# -------------------------
# Save cleaned data
# -------------------------
df.to_csv(CLEAN_FILE, index=False)
print(f"Cleaned customers data saved to {CLEAN_FILE}")
print(f"Final cleaned shape: {df.shape}")
