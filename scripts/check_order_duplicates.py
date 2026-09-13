import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

file = os.path.join(
    project_root,
    "cleaned_data",
    "Shopify_orders_clean.csv"
)

df = pd.read_csv(file)

counts = df["Order ID"].value_counts()

duplicates = counts[counts > 1]

print("=" * 60)
print("ORDER DUPLICATE CHECK")
print("=" * 60)

print("Total order rows:", len(df))
print("Unique Order IDs:", df["Order ID"].nunique())
print("Duplicate Order IDs:", len(duplicates))

print("\nDuplicate orders:")

if len(duplicates) > 0:
    for order_id in duplicates.index:
        print("\nORDER:", order_id)

        print(
            df[df["Order ID"] == order_id][
                [
                    "Order ID",
                    "Order Name",
                    "Total Sales (INR)",
                    "Net Sales (INR)",
                    "Orders",
                    "Product Title"
                ]
            ].to_string(index=False)
        )
else:
    print("No duplicate Order IDs found.")

print("=" * 60)