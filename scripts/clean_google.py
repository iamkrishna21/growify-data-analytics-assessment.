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
    "Google_Ads_data.csv"
)

output_dir = os.path.join(
    project_root,
    "cleaned_data"
)

os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    "Google_Ads_clean.csv"
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
# 2. REMOVE EMPTY COLUMNS
# ============================================================

empty_columns = df.columns[
    df.isna().all()
].tolist()

print("\nCompletely empty columns:")
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
# 4. CLEAN TEXT
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
# 5. DATE
# ============================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

# ============================================================
# 6. NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "Cost (INR)",
    "Clicks",
    "Impressions",
    "CPC (INR)",
    "CTR",
    "CPM (INR)",
    "Conversions",
    "Conv. Value (INR)"
]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# ============================================================
# 7. DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

print(
    "\nDuplicate rows:",
    duplicate_count
)

df = df.drop_duplicates()

# ============================================================
# 8. DO NOT IMPUTE CPC BLINDLY
# ============================================================
#
# CPC can be missing when there are zero clicks.
# We calculate our own CPC instead.
#
# CPC = Cost / Clicks

df["CPC_Calculated"] = np.where(
    df["Clicks"] > 0,
    df["Cost (INR)"] / df["Clicks"],
    np.nan
)

# ============================================================
# 9. CALCULATE CTR
# ============================================================

df["CTR_Calculated"] = np.where(
    df["Impressions"] > 0,
    df["Clicks"] / df["Impressions"],
    np.nan
)

# ============================================================
# 10. CALCULATE CPM
# ============================================================

df["CPM_Calculated"] = np.where(
    df["Impressions"] > 0,
    (df["Cost (INR)"] / df["Impressions"]) * 1000,
    np.nan
)

# ============================================================
# 11. VALIDATION
# ============================================================

print("\nNegative values:")

for col in numeric_columns:

    if col in df.columns:

        count = (df[col] < 0).sum()

        if count > 0:
            print(
                f"{col}: {count}"
            )

# ============================================================
# 12. INVALID DATE CHECK
# ============================================================

print(
    "\nInvalid dates:",
    df["Date"].isna().sum()
)

# ============================================================
# 13. SORT
# ============================================================

df = df.sort_values(
    by=[
        "Date",
        "Campaign"
    ]
).reset_index(drop=True)

# ============================================================
# 14. SAVE
# ============================================================

df.to_csv(
    output_file,
    index=False
)

print("\n========================================")
print("GOOGLE CLEANING COMPLETE")
print("========================================")
print("Final shape:", df.shape)
print("Saved to:")
print(output_file)