import pandas as pd


def detect_customer_churn(customers):

    churn_risk = customers[
        customers["last_purchase_days"] >= 90
    ]

    potential_revenue = churn_risk["total_spend"].sum()

    return {
        "count": len(churn_risk),
        "potential_revenue": potential_revenue
    }


def detect_product_opportunities(products):

    products = products.copy()

    products["conversion_rate"] = (
        products["orders"]
        / products["views"].replace(0, 1)
    ) * 100

    opportunities = products[
        (products["views"] >= 5000)
        & (products["conversion_rate"] < 2)
    ]

    return {
        "count": len(opportunities),
        "products": opportunities
    }


def detect_payment_failures(transactions):

    total_transactions = len(transactions)

    failed_transactions = transactions[
        transactions["status"] == "Failed"
    ]

    failed_count = len(failed_transactions)

    failure_rate = (
        failed_count / total_transactions * 100
        if total_transactions > 0
        else 0
    )

    return {
        "failed_count": failed_count,
        "failure_rate": failure_rate
    }


def calculate_budget_plan(budget, goal):

    if goal == "Increase Revenue":

        return {
            "Customer Retargeting": budget * 0.40,
            "Product Promotion": budget * 0.35,
            "A/B Testing": budget * 0.25
        }

    elif goal == "Improve Customer Retention":

        return {
            "Win-back Campaign": budget * 0.50,
            "Customer Incentives": budget * 0.30,
            "A/B Testing": budget * 0.20
        }

    elif goal == "Recover Failed Payments":

        return {
            "Payment Retry": budget * 0.50,
            "Recovery Campaign": budget * 0.30,
            "Testing": budget * 0.20
        }

    else:

        return {
            "Product Promotion": budget * 0.50,
            "Offers": budget * 0.30,
            "A/B Testing": budget * 0.20
        }


def generate_growth_opportunities(
    customers,
    products,
    transactions,
    goal="Increase Revenue",
    budget=50000,
    duration=14,
    target_segment="All Customers"
):

    opportunities = []

    churn = detect_customer_churn(customers)

    product_result = detect_product_opportunities(products)

    payment_result = detect_payment_failures(transactions)

    budget_plan = calculate_budget_plan(
        budget,
        goal
    )

    # -----------------------------------------
    # CUSTOMER RETENTION
    # -----------------------------------------

    if goal == "Improve Customer Retention":

        if churn["count"] > 0:

            opportunities.append({

                "type": "Customer Retention",

                "priority": "High",

                "description": (
                    f"{churn['count']} customers have been "
                    "inactive for 90+ days."
                ),

                "potential_value":
                    churn["potential_revenue"],

                "action": (
                    f"Launch a {duration}-day win-back "
                    f"campaign targeting {target_segment.lower()}."
                ),

                "budget_plan": budget_plan
            })


    # -----------------------------------------
    # REVENUE GROWTH
    # -----------------------------------------

    elif goal == "Increase Revenue":

        opportunities.append({

            "type": "Revenue Expansion",

            "priority": "High",

            "description": (
                "Customer and product behaviour indicates "
                "multiple opportunities for revenue expansion."
            ),

            "potential_value":
                churn["potential_revenue"],

            "action": (
                f"Run a {duration}-day revenue campaign "
                "using retargeting, cross-selling and "
                "high-value customer offers."
            ),

            "budget_plan": budget_plan
        })


    # -----------------------------------------
    # PAYMENT RECOVERY
    # -----------------------------------------

    elif goal == "Recover Failed Payments":

        if payment_result["failure_rate"] >= 10:

            opportunities.append({

                "type": "Payment Recovery",

                "priority": "High",

                "description": (
                    f"Payment failure rate is "
                    f"{payment_result['failure_rate']:.1f}%."
                ),

                "potential_value": 0,

                "action": (
                    f"Run a {duration}-day payment recovery "
                    "strategy using retries and alternative "
                    "payment methods."
                ),

                "budget_plan": budget_plan
            })


    # -----------------------------------------
    # PRODUCT CONVERSION
    # -----------------------------------------

    elif goal == "Increase Product Conversion":

        if product_result["count"] > 0:

            opportunities.append({

                "type": "Product Conversion",

                "priority": "High",

                "description": (
                    f"{product_result['count']} products have "
                    "high traffic but low conversion."
                ),

                "potential_value": 0,

                "action": (
                    f"Run a {duration}-day conversion campaign "
                    "using pricing experiments, offers and "
                    "better product messaging."
                ),

                "budget_plan": budget_plan
            })


    return opportunities