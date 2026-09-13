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
    "Facebook_Ads_data.csv"
)

output_dir = os.path.join(
    project_root,
    "cleaned_data"
)

os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    "Facebook_Ads_clean.csv"
)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(input_file, low_memory=False)

print("Original shape:", df.shape)

# ============================================================
# 1. REMOVE COMPLETELY EMPTY ROWS
# ============================================================

df = df.dropna(axis=0, how="all")

# ============================================================
# 2. REMOVE COMPLETELY EMPTY COLUMNS
# ============================================================

empty_columns = df.columns[df.isna().all()].tolist()

print("\nCompletely empty columns removed:")
print(empty_columns)

df = df.dropna(axis=1, how="all")

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
# 5. CONVERT DATE
# ============================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

# ============================================================
# 6. CONVERT DATETIME COLUMNS
# ============================================================

datetime_columns = [
    "Ad set Start Time",
    "Ad Start Time",
    "Campaign Start Time",
    "Ad End Time",
    "Ad set End Time",
    "Campaign End Time"
]

for col in datetime_columns:

    if col in df.columns:

        df[col] = pd.to_datetime(
            df[col],
            errors="coerce",
            utc=True
        )

# ============================================================
# 7. CONVERT NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "FB Spent Funnel (INR)",
    "Amount Spent (INR)",
    "Clicks (all)",
    "Impressions",
    "Page Likes",
    "Landing Page Views",
    "Link Clicks",
    "Adds to Cart",
    "Checkouts Initiated",
    "Adds of Payment Info",
    "Purchases",
    "Purchases Conversion Value (INR)",
    "Website Contacts",
    "Messaging Conversations Started",
    "Adds to Cart Conversion Value (INR)",
    "Checkouts Initiated Conversion Value (INR)",
    "Adds of Payment Info Conversion Value (INR)",
    "Row Count",
    "Ad Account ID",
    "Campaign Result value"
]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# ============================================================
# 8. EVENT METRICS
# ============================================================
# For Meta reporting, blank event fields generally represent
# no recorded event. We therefore convert missing event/value
# metrics to zero.
#
# We DO NOT replace missing metadata with zero.

event_columns = [
    "Page Likes",
    "Landing Page Views",
    "Link Clicks",
    "Checkouts Initiated",
    "Adds of Payment Info",
    "Purchases",
    "Purchases Conversion Value (INR)",
    "Messaging Conversations Started",
    "Checkouts Initiated Conversion Value (INR)",
    "Adds of Payment Info Conversion Value (INR)"
]

for col in event_columns:

    if col in df.columns:
        df[col] = df[col].fillna(0)

# ============================================================
# 9. CHECK DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows found:", duplicate_count)

# Remove exact duplicates only.
df = df.drop_duplicates()

# ============================================================
# 10. BASIC DATA VALIDATION
# ============================================================

print("\nNegative values check:")

for col in numeric_columns:

    if col in df.columns:

        negative_count = (df[col] < 0).sum()

        if negative_count > 0:

            print(
                f"{col}: {negative_count}"
            )

# ============================================================
# 11. INVALID DATE CHECK
# ============================================================

print(
    "\nInvalid Date values:",
    df["Date"].isna().sum()
)

# ============================================================
# 12. CREATE CLEAN SPEND COLUMN
# ============================================================
# Keep original Facebook spend columns.
# This creates a standard field for future analysis.

if "Amount Spent (INR)" in df.columns:

    df["Spend (INR)"] = df["Amount Spent (INR)"]

# ============================================================
# 13. SORT
# ============================================================

sort_columns = [
    col for col in
    ["Date", "Campaign Name", "Ad Set Name", "Ad Name"]
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
print("FACEBOOK CLEANING COMPLETE")
print("========================================")
print("Final shape:", df.shape)
print("Saved to:")
print(output_file)