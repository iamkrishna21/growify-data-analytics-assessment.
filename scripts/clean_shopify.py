import pandas as pd
import numpy as np
import os

# ============================================================
# PATH SETUP
# ============================================================

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_file = os.path.join(
    project_root,
    "raw_data",
    "Shopify_sales_data.csv"
)

output_dir = os.path.join(
    project_root,
    "cleaned_data"
)

os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    "Shopify_sales_clean.csv"
)

# ============================================================
# LOAD
# ============================================================

df = pd.read_csv(
    input_file,
    low_memory=False
)

print("Original shape:", df.shape)

# ============================================================
# 1. REMOVE EMPTY ROWS
# ============================================================

df = df.dropna(
    axis=0,
    how="all"
)

# ============================================================
# 2. REMOVE 100% EMPTY COLUMNS
# ============================================================

empty_columns = df.columns[
    df.isna().all()
].tolist()

print("\nCompletely empty columns removed:")
print(empty_columns)

df = df.dropna(
    axis=1,
    how="all"
)

# ============================================================
# 3. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# ============================================================
# 4. CLEAN TEXT COLUMNS
# ============================================================

text_columns = df.select_dtypes(
    include=["object", "string"]
).columns

for col in text_columns:

    df[col] = (
        df[col]
        .astype("string")
        .str.strip()
    )

# ============================================================
# 5. DATE COLUMNS
# ============================================================

date_columns = [
    "Date",
    "Transaction Timestamp",
    "Order Created At",
    "Order Updated At"
]

for col in date_columns:

    if col in df.columns:

        df[col] = pd.to_datetime(
            df[col],
            errors="coerce",
            utc=True
        )

# ============================================================
# 6. NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "Order ID",
    "Product ID",
    "Gross Sales (INR)",
    "Net Sales (INR)",
    "Total Sales (INR)",
    "Orders",
    "Returns (INR)",
    "Return Rate",
    "Items Sold",
    "Items Returned",
    "Average Order Value (INR)",
    "New Customer Orders",
    "Returning Customer Orders",
    "Average Items Per Order",
    "Discounts (INR)",
    "Row Count",
    "SKU",
    "Customer ID"
]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# ============================================================
# 7. DUPLICATE CHECK
# ============================================================

duplicate_count = df.duplicated().sum()

print(
    "\nExact duplicate rows:",
    duplicate_count
)

# Remove ONLY exact duplicate rows.
df = df.drop_duplicates()

# ============================================================
# 8. ORDER STRUCTURE CHECK
# ============================================================

if "Order ID" in df.columns:

    order_counts = (
        df["Order ID"]
        .value_counts()
    )

    multiple_row_orders = (
        order_counts > 1
    ).sum()

    print(
        "Orders appearing on multiple rows:",
        multiple_row_orders
    )

# ============================================================
# 9. DO NOT FILL SALES WITH ZERO
# ============================================================
#
# Gross/Net/Total Sales contain 0 legitimately.
# Missing and zero are different concepts.
#
# Therefore we leave sales NULL if genuinely missing.

# ============================================================
# 10. CREATE BASIC DATA QUALITY FLAGS
# ============================================================

df["Missing_Product_Info"] = (
    df["Product ID"].isna()
)

df["Missing_Customer_ID"] = (
    df["Customer ID"].isna()
)

# ============================================================
# 11. NEGATIVE VALUE CHECK
# ============================================================

print("\nNegative value check:")

for col in [
    "Gross Sales (INR)",
    "Net Sales (INR)",
    "Total Sales (INR)",
    "Returns (INR)",
    "Discounts (INR)"
]:

    if col in df.columns:

        count = (
            df[col] < 0
        ).sum()

        if count > 0:

            print(
                f"{col}: {count}"
            )

# ============================================================
# 12. CHECK IMPORTANT SALES COLUMNS
# ============================================================

print("\nMissing sales values:")

for col in [
    "Gross Sales (INR)",
    "Net Sales (INR)",
    "Total Sales (INR)",
    "Orders"
]:

    if col in df.columns:

        print(
            col,
            ":",
            df[col].isna().sum()
        )

# ============================================================
# 13. SORT
# ============================================================

sort_columns = [
    col for col in
    ["Date", "Order ID"]
    if col in df.columns
]

df = df.sort_values(
    by=sort_columns
).reset_index(drop=True)

# ============================================================
# 14. SAVE
# ============================================================

df.to_csv(
    output_file,
    index=False
)

print("\n========================================")
print("SHOPIFY CLEANING COMPLETE")
print("========================================")
print("Final shape:", df.shape)
print("Saved to:")
print(output_file)