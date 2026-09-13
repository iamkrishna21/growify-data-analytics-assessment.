import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_file = os.path.join(
    project_root,
    "cleaned_data",
    "Shopify_orders_clean.csv"
)

output_file = os.path.join(
    project_root,
    "cleaned_data",
    "Shopify_final.csv"
)

df = pd.read_csv(input_file)

# Each Order Name represents a separate order
df = df.drop_duplicates(subset=["Order Name"], keep="first")

df.to_csv(output_file, index=False)

print("=" * 60)
print("FINAL SHOPIFY DATASET")
print("=" * 60)

print("Rows:", len(df))
print("Unique Order Names:", df["Order Name"].nunique())

print("Total Sales:", df["Total Sales (INR)"].sum())
print("Net Sales:", df["Net Sales (INR)"].sum())

print("\nSaved to:")
print(output_file)