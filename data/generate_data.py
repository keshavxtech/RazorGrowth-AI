import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# -----------------------------
# 1. CUSTOMERS
# -----------------------------

num_customers = 2000

customers = []

locations = [
    "Delhi", "Mumbai", "Bangalore", "Hyderabad",
    "Pune", "Chennai", "Kolkata", "Noida"
]

for i in range(1, num_customers + 1):

    signup_date = datetime(2025, 1, 1) + timedelta(
        days=random.randint(0, 500)
    )

    customers.append({
        "customer_id": f"CUST{i:04d}",
        "age": random.randint(18, 55),
        "location": random.choice(locations),
        "signup_date": signup_date.date(),
        "total_orders": random.randint(1, 30),
        "total_spend": round(random.uniform(500, 100000), 2),
        "last_purchase_days": random.randint(1, 180)
    })

customers_df = pd.DataFrame(customers)


# -----------------------------
# 2. PRODUCTS
# -----------------------------

num_products = 100

categories = [
    "Electronics",
    "Fashion",
    "Beauty",
    "Home",
    "Sports"
]

products = []

for i in range(1, num_products + 1):

    views = random.randint(500, 20000)
    orders = random.randint(20, min(views, 1000))

    products.append({
        "product_id": f"PROD{i:03d}",
        "product_name": f"Product {i}",
        "category": random.choice(categories),
        "price": round(random.uniform(199, 15000), 2),
        "views": views,
        "orders": orders,
        "inventory": random.randint(0, 500)
    })

products_df = pd.DataFrame(products)


# -----------------------------
# 3. TRANSACTIONS
# -----------------------------

num_transactions = 10000

transactions = []

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Wallet"
]

statuses = [
    "Success",
    "Success",
    "Success",
    "Success",
    "Failed"
]

start_date = datetime(2026, 1, 1)

for i in range(1, num_transactions + 1):

    customer_id = f"CUST{random.randint(1, num_customers):04d}"
    product_id = f"PROD{random.randint(1, num_products):03d}"

    amount = round(random.uniform(200, 20000), 2)

    transaction_date = start_date + timedelta(
        days=random.randint(0, 230)
    )

    transactions.append({
        "transaction_id": f"TXN{i:05d}",
        "customer_id": customer_id,
        "product_id": product_id,
        "amount": amount,
        "payment_method": random.choice(payment_methods),
        "status": random.choice(statuses),
        "transaction_date": transaction_date.date()
    })

transactions_df = pd.DataFrame(transactions)


# -----------------------------
# 4. CAMPAIGNS
# -----------------------------

num_campaigns = 50

campaign_types = [
    "Reactivation",
    "Product Promotion",
    "Discount",
    "Upsell",
    "Cross Sell"
]

campaigns = []

for i in range(1, num_campaigns + 1):

    targeted = random.randint(100, 1000)
    conversions = random.randint(5, int(targeted * 0.25))
    revenue = round(
        conversions * random.uniform(500, 3000),
        2
    )

    campaigns.append({
        "campaign_id": f"CAMP{i:03d}",
        "campaign_type": random.choice(campaign_types),
        "targeted_customers": targeted,
        "conversions": conversions,
        "revenue_generated": revenue
    })

campaigns_df = pd.DataFrame(campaigns)


# -----------------------------
# SAVE DATA
# -----------------------------

customers_df.to_csv("data/customers.csv", index=False)
products_df.to_csv("data/products.csv", index=False)
transactions_df.to_csv("data/transactions.csv", index=False)
campaigns_df.to_csv("data/campaigns.csv", index=False)

print("===================================")
print("RazorGrowth AI Dataset Generated!")
print("===================================")

print(f"Customers: {len(customers_df)}")
print(f"Products: {len(products_df)}")
print(f"Transactions: {len(transactions_df)}")
print(f"Campaigns: {len(campaigns_df)}")