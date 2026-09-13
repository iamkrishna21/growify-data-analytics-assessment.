import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

cleaned = os.path.join(project_root, "cleaned_data")
output = os.path.join(cleaned, "master_marketing_data.csv")

# Load datasets
facebook = pd.read_csv(os.path.join(cleaned, "Facebook_Ads_clean.csv"))
google = pd.read_csv(os.path.join(cleaned, "Google_Ads_clean.csv"))
shopify = pd.read_csv(os.path.join(cleaned, "Shopify_final.csv"))

# Standardise column names
facebook["Platform"] = "Facebook"
google["Platform"] = "Google"

# Facebook
fb = facebook.rename(columns={
    "Campaign Name": "Campaign",
    "Amount Spent (INR)": "Spend (INR)",
    "Purchases Conversion Value (INR)": "Revenue (INR)",
    "Clicks (all)": "Clicks"
})

fb = fb[
    [
        "Date",
        "Platform",
        "Campaign",
        "Spend (INR)",
        "Revenue (INR)",
        "Clicks",
        "Impressions",
        "Purchases"
    ]
]

# Remove any duplicate columns in Facebook data
fb = fb.loc[:, ~fb.columns.duplicated(keep='first')]

# Google
gg = google.rename(columns={
    "Cost (INR)": "Spend (INR)",
    "Conv. Value (INR)": "Revenue (INR)"
})

gg["Purchases"] = gg["Conversions"]

gg = gg[
    [
        "Date",
        "Platform",
        "Campaign",
        "Spend (INR)",
        "Revenue (INR)",
        "Clicks",
        "Impressions",
        "Purchases"
    ]
]

# Combine advertising data - reset indices to avoid reindexing issues
ads = pd.concat([fb.reset_index(drop=True), gg.reset_index(drop=True)], ignore_index=True)

# Clean numeric columns
numeric_cols = [
    "Spend (INR)",
    "Revenue (INR)",
    "Clicks",
    "Impressions",
    "Purchases"
]

for col in numeric_cols:
    ads[col] = pd.to_numeric(ads[col], errors="coerce").fillna(0)

ads.to_csv(output, index=False)

print("=" * 60)
print("MASTER MARKETING DATA CREATED")
print("=" * 60)

print("Facebook rows:", len(fb))
print("Google rows:", len(gg))
print("Master rows:", len(ads))

print("\nTotal Ad Spend:", ads["Spend (INR)"].sum())
print("Total Ad Revenue:", ads["Revenue (INR)"].sum())
print("Total Purchases:", ads["Purchases"].sum())

print("\nSaved to:")
print(output)