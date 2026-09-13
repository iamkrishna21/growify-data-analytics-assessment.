import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_file = os.path.join(
    project_root,
    "cleaned_data",
    "master_marketing_data.csv"
)

output_file = os.path.join(
    project_root,
    "cleaned_data",
    "marketing_metrics.csv"
)

df = pd.read_csv(input_file)

# Core metrics
df["ROAS"] = df["Revenue (INR)"] / df["Spend (INR)"].replace(0, pd.NA)

df["CTR"] = (
    df["Clicks"] / df["Impressions"].replace(0, pd.NA)
) * 100

df["CPC (INR)"] = (
    df["Spend (INR)"] / df["Clicks"].replace(0, pd.NA)
)

df["CPM (INR)"] = (
    df["Spend (INR)"] / df["Impressions"].replace(0, pd.NA)
) * 1000

df["Conversion Rate"] = (
    df["Purchases"] / df["Clicks"].replace(0, pd.NA)
) * 100

df["AOV (INR)"] = (
    df["Revenue (INR)"] / df["Purchases"].replace(0, pd.NA)
)

df.to_csv(output_file, index=False)

print("=" * 60)
print("MARKETING METRICS CREATED")
print("=" * 60)

print("\nOverall metrics:")

total_spend = df["Spend (INR)"].sum()
total_revenue = df["Revenue (INR)"].sum()
total_clicks = df["Clicks"].sum()
total_impressions = df["Impressions"].sum()
total_purchases = df["Purchases"].sum()

print("Spend:", total_spend)
print("Revenue:", total_revenue)
print("ROAS:", total_revenue / total_spend)
print("CTR:", (total_clicks / total_impressions) * 100)
print("CPC:", total_spend / total_clicks)
print("CPM:", (total_spend / total_impressions) * 1000)
print("Purchases:", total_purchases)
print("Conversion Rate:", (total_purchases / total_clicks) * 100)
print("AOV:", total_revenue / total_purchases)

print("\nBy Platform:")

platform = df.groupby("Platform").agg({
    "Spend (INR)": "sum",
    "Revenue (INR)": "sum",
    "Clicks": "sum",
    "Impressions": "sum",
    "Purchases": "sum"
})

platform["ROAS"] = (
    platform["Revenue (INR)"] / platform["Spend (INR)"]
)

print(platform)

print("\nSaved to:")
print(output_file)