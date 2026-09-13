import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_file = os.path.join(
    project_root,
    "cleaned_data",
    "Facebook_Ads_clean.csv"
)

output_file = os.path.join(
    project_root,
    "cleaned_data",
    "Facebook_analysis.csv"
)

df = pd.read_csv(input_file)

df = df.rename(columns={
    "Campaign Name": "Campaign",
    "Purchases Conversion Value (INR)": "Revenue (INR)"
})

# Use existing "Spend (INR)" column
df["Spend (INR)"] = pd.to_numeric(
    df["Spend (INR)"], errors="coerce"
).fillna(0)

df["Revenue (INR)"] = pd.to_numeric(
    df["Revenue (INR)"], errors="coerce"
).fillna(0)

df["Purchases"] = pd.to_numeric(
    df["Purchases"], errors="coerce"
).fillna(0)

df["Clicks"] = pd.to_numeric(
    df["Clicks (all)"], errors="coerce"
).fillna(0)

df["Impressions"] = pd.to_numeric(
    df["Impressions"], errors="coerce"
).fillna(0)

df["ROAS"] = (
    df["Revenue (INR)"] /
    df["Spend (INR)"].replace(0, pd.NA)
)

df["CTR"] = (
    df["Clicks"] /
    df["Impressions"].replace(0, pd.NA)
) * 100

df.to_csv(output_file, index=False)

print("=" * 60)
print("FACEBOOK ANALYSIS FILE CREATED")
print("=" * 60)

print("Rows:", len(df))
print("Campaigns:", df["Campaign"].nunique())
print("Ad Sets:", df["Ad Set Name"].nunique())
print("Ads:", df["Ad Name"].nunique())

print("\nSaved to:")
print(output_file)