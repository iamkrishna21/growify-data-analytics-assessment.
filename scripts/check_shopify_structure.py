import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

file = os.path.join(
    project_root,
    "cleaned_data",
    "Shopify_sales_clean.csv"
)

df = pd.read_csv(file)

print("=" * 60)
print("SHOPIFY CHECK")
print("=" * 60)

print("\nTotal rows:", len(df))

print(
    "Unique Order IDs:",
    df["Order ID"].nunique()
)

print(
    "Rows with multiple products/orders:",
    (df["Order ID"].value_counts() > 1).sum()
)

print("\nSample orders with multiple rows:")

counts = df["Order ID"].value_counts()

multi_orders = counts[counts > 1].head(5).index

for order_id in multi_orders:

    print("\nORDER:", order_id)

    print(
        df[df["Order ID"] == order_id][
            [
                "Order ID",
                "Order Name",
                "Product ID",
                "Product Title",
                "Gross Sales (INR)",
                "Net Sales (INR)",
                "Total Sales (INR)",
                "Orders"
            ]
        ].to_string(index=False)
    )

print("\n" + "=" * 60)
print("TOTAL SALES CHECK")
print("=" * 60)

print(
    "Sum of Total Sales:",
    df["Total Sales (INR)"].sum()
)

print(
    "Sum of Net Sales:",
    df["Net Sales (INR)"].sum()
)

print(
    "Sum of Orders:",
    df["Orders"].sum()
)

print(
    "Unique Order IDs:",
    df["Order ID"].nunique()
)