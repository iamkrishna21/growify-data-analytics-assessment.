import pandas as pd
import os

# =========================
# FILE PATHS
# =========================

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root (parent of scripts folder)
project_root = os.path.dirname(script_dir)

files = {
    "facebook": os.path.join(project_root, "raw_data", "Facebook_Ads_data.csv"),
    "google": os.path.join(project_root, "raw_data", "Google_Ads_data.csv"),
    "shopify": os.path.join(project_root, "raw_data", "Shopify_sales_data.csv")
}

# =========================
# INSPECTION FUNCTION
# =========================

def inspect_data(name, file_path):

    print("\n" + "=" * 80)
    print(f"{name.upper()} DATASET")
    print("=" * 80)

    df = pd.read_csv(file_path)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nNumeric summary:")
    print(df.describe(include="number").T)

    return df


facebook_raw = inspect_data(
    "Facebook",
    files["facebook"]
)

google_raw = inspect_data(
    "Google",
    files["google"]
)

shopify_raw = inspect_data(
    "Shopify",
    files["shopify"]
)