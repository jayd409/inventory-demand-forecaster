import sys
sys.path.insert(0, 'src')

from config import config
from data import generate_inventory
from forecast import reorder_report
from charts import (top_sku_trends, category_revenue, stockout_risk,
                    seasonal_heatmap, stock_vs_demand, forecast_vs_actual)
from utils import save_html
from database import save_to_db, query

# Calculate weeks from months_of_data (52 weeks/year)
weeks = config['months_of_data'] * 4
df = generate_inventory(weeks=weeks)
save_to_db(df, 'inventory')

reorder_df = reorder_report(df)
reorder_df.to_csv('outputs/reorder_report.csv', index=False)
print(f"  Saved → outputs/reorder_report.csv")

charts = [
    ('Top 5 SKU Trends', top_sku_trends(df)),
    ('Revenue by Category', category_revenue(df)),
    ('Stockout Risk', stockout_risk(reorder_df)),
    ('Seasonal Demand Heatmap', seasonal_heatmap(df)),
    ('Stock vs Demand', stock_vs_demand(df)),
    ('Forecast vs Actual', forecast_vs_actual(df))
]

reorder_count = reorder_df['reorder_needed'].sum()
highest_risk = reorder_df.iloc[0]['sku_id'] if len(reorder_df) > 0 else 'N/A'

kpis = [
    ('SKUs Needing Reorder', str(int(reorder_count))),
    ('Highest Risk SKU', highest_risk),
    ('Total SKUs', str(len(reorder_df))),
]

save_html(charts, 'Inventory Demand Forecasting', kpis, 'outputs/inventory_dashboard.html')

print(f"\nSKUs needing reorder: {reorder_count} | Highest risk: {highest_risk}")
