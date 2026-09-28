# Sales & Retail Data Analysis Dashboard

Cleans a messy raw retail sales export (inconsistent casing, stray
whitespace, missing values) with Python/Pandas, computes key business
metrics, and produces chart images. The cleaned CSV is designed to be
loaded straight into **Power BI** or **Excel** for an interactive
dashboard.

## Files
- `raw_sales_data.csv` — sample raw export (800 orders, intentionally messy)
- `clean_and_analyze.py` — cleaning + analysis + chart generation
- `cleaned_sales_data.csv` — output: clean, analysis-ready dataset
- `chart_monthly_sales.png`, `chart_sales_by_category.png`,
  `chart_profit_margin_by_region.png` — output charts

## What the cleaning step does
- Normalizes inconsistent text casing/whitespace in `Region`, `Category`, `SubCategory`
- Parses `OrderDate` into proper datetime
- Recomputes missing `Sales` values from `Quantity × UnitPrice × (1 − Discount)`
- Drops duplicate rows
- Adds a `Month` column and a `ProfitMargin` column for easier aggregation

## How to run
```bash
pip install pandas matplotlib
python clean_and_analyze.py
```

## Building the Power BI dashboard
1. Open Power BI Desktop → **Get Data → Text/CSV** → select `cleaned_sales_data.csv`.
2. Suggested visuals:
   - Line chart: `Month` vs `Sales` (trend)
   - Bar chart: `Category` vs `Sales`
   - Map or bar chart: `Region` vs `Sales`
   - Card visuals: Total Sales, Total Profit, Order Count
   - Slicer: `Region`, `Category`, date range on `OrderDate`
3. Add a measure for profit margin: `Profit Margin = SUM(Profit) / SUM(Sales)`

## Skills demonstrated
Data cleaning, handling missing/messy data, Pandas aggregation,
matplotlib visualization, and structuring a dataset for BI tools.
