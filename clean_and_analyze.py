"""
Sales & Retail Data Analysis
----------------------------
Cleans a messy raw retail sales export, computes key business metrics,
and produces summary charts + a cleaned CSV that can be loaded straight
into Power BI / Excel for dashboarding.

Run:
    python clean_and_analyze.py
"""
import pandas as pd
import matplotlib.pyplot as plt

RAW_FILE = "raw_sales_data.csv"
CLEAN_FILE = "cleaned_sales_data.csv"


def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # 1. Normalize text fields (fix stray whitespace / inconsistent casing)
    df["Region"] = df["Region"].str.strip().str.title()
    df["Category"] = df["Category"].str.strip().str.title()
    df["SubCategory"] = df["SubCategory"].str.strip().str.title()

    # 2. Parse dates
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])

    # 3. Handle missing Sales values — recompute from Quantity * UnitPrice * (1-Discount)
    recomputed = df["Quantity"] * df["UnitPrice"] * (1 - df["Discount"])
    df["Sales"] = df["Sales"].fillna(round(recomputed, 2))

    # 4. Drop exact duplicate rows, if any
    df = df.drop_duplicates()

    # 5. Add helper columns used by the dashboard
    df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
    df["ProfitMargin"] = (df["Profit"] / df["Sales"]).round(3)

    return df


def summarize(df: pd.DataFrame) -> None:
    print("=== Overall ===")
    print(f"Total Sales:  {df['Sales'].sum():,.2f}")
    print(f"Total Profit: {df['Profit'].sum():,.2f}")
    print(f"Orders:       {df['OrderID'].nunique():,}")
    print()

    print("=== Sales by Region ===")
    print(df.groupby("Region")["Sales"].sum().sort_values(ascending=False).round(2))
    print()

    print("=== Sales by Category ===")
    print(df.groupby("Category")["Sales"].sum().sort_values(ascending=False).round(2))
    print()

    print("=== Top 5 Months by Sales ===")
    print(df.groupby("Month")["Sales"].sum().sort_values(ascending=False).head(5).round(2))


def make_charts(df: pd.DataFrame) -> None:
    # Chart 1: Monthly sales trend
    monthly = df.groupby("Month")["Sales"].sum().sort_index()
    plt.figure(figsize=(9, 4))
    monthly.plot(kind="line", marker="o")
    plt.title("Monthly Sales Trend")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("chart_monthly_sales.png", dpi=150)
    plt.close()

    # Chart 2: Sales by category
    by_cat = df.groupby("Category")["Sales"].sum().sort_values()
    plt.figure(figsize=(6, 4))
    by_cat.plot(kind="barh", color="#1F4E79")
    plt.title("Total Sales by Category")
    plt.xlabel("Sales")
    plt.tight_layout()
    plt.savefig("chart_sales_by_category.png", dpi=150)
    plt.close()

    # Chart 3: Region vs profit margin
    by_region = df.groupby("Region")["ProfitMargin"].mean().sort_values()
    plt.figure(figsize=(6, 4))
    by_region.plot(kind="bar", color="#2E7D32")
    plt.title("Average Profit Margin by Region")
    plt.ylabel("Profit Margin")
    plt.tight_layout()
    plt.savefig("chart_profit_margin_by_region.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    df = load_and_clean(RAW_FILE)
    df.to_csv(CLEAN_FILE, index=False)
    summarize(df)
    make_charts(df)
    print(f"\nCleaned data written to {CLEAN_FILE}")
    print("Charts saved: chart_monthly_sales.png, chart_sales_by_category.png, "
          "chart_profit_margin_by_region.png")
