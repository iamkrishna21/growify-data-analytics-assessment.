import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_file = os.path.join(
    project_root,
    "cleaned_data",
    "Shopify_sales_clean.csv"
)

output_file = os.path.join(
    project_root,
    "cleaned_data",
    "Shopify_orders_clean.csv"
)

df = pd.read_csv(input_file)

# Keep only rows representing actual orders
orders = df[df["Orders"] == 1].copy()

# Save order-level dataset
orders.to_csv(output_file, index=False)

print("=" * 60)
print("SHOPIFY ORDER DATASET CREATED")
print("=" * 60)

print("Original rows:", len(df))
print("Order rows:", len(orders))
print("Unique Order IDs:", orders["Order ID"].nunique())

print(
    "Total Sales:",
    orders["Total Sales (INR)"].sum()
)

print(
    "Net Sales:",
    orders["Net Sales (INR)"].sum()
)

print(
    "Orders:",
    orders["Orders"].sum()
)

print("\nSaved to:")
print(output_file)