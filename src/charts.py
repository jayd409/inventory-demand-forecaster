import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from forecast import forecast_sku, reorder_report

def top_sku_trends(df):
    """Chart 1: Top 5 SKU demand trends over 2 years."""
    top_skus = df.groupby('sku_id')['units_sold'].sum().nlargest(5).index
    fig, ax = plt.subplots(figsize=(10, 5))
    for sku in top_skus:
        sku_data = df[df['sku_id'] == sku].sort_values('week')
        ax.plot(sku_data['week'], sku_data['units_sold'], label=sku, marker='o', markersize=3)
    ax.set_title('Top 5 SKU Demand Trends (2 Years)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Week')
    ax.set_ylabel('Units Sold')
    ax.legend(loc='best', fontsize=8)
    return fig

def category_revenue(df):
    """Chart 2: Category revenue breakdown."""
    cat_revenue = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(cat_revenue.index, cat_revenue.values, color='steelblue')
    ax.set_title('Total Revenue by Category', fontsize=12, fontweight='bold')
    ax.set_xlabel('Category')
    ax.set_ylabel('Revenue ($)')
    ax.tick_params(axis='x', rotation=45)
    return fig

def stockout_risk(reorder_df):
    """Chart 3: Stockout risk (weeks of coverage)."""
    reorder_df_sorted = reorder_df.sort_values('weeks_coverage')[:15]
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['red' if x < 3 else 'orange' if x < 5 else 'green' for x in reorder_df_sorted['weeks_coverage']]
    ax.barh(reorder_df_sorted['sku_id'], reorder_df_sorted['weeks_coverage'], color=colors)
    ax.axvline(x=3, color='darkred', linestyle='--', linewidth=2, label='Reorder threshold')
    ax.set_title('Stock Coverage by SKU (Highest Risk)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Weeks of Coverage')
    ax.legend()
    return fig

def seasonal_heatmap(df):
    """Chart 4: Seasonal demand heatmap (category × month)."""
    df_copy = df.copy()
    df_copy['month'] = pd.to_datetime(df_copy['date']).dt.month
    pivot = df_copy.pivot_table(values='units_sold', index='category', columns='month', aggfunc='sum')
    fig, ax = plt.subplots(figsize=(10, 5))
    im = ax.imshow(pivot.fillna(0), cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(12))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    ax.set_title('Seasonal Demand Heatmap', fontsize=12, fontweight='bold')
    ax.set_xlabel('Month')
    plt.colorbar(im, ax=ax)
    return fig

def stock_vs_demand(df):
    """Chart 5: Stock level vs demand scatter."""
    scatter_data = df.groupby('sku_id').agg({'stock_level': 'mean', 'units_sold': 'mean'}).reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(scatter_data['units_sold'], scatter_data['stock_level'], alpha=0.6, s=100, color='teal')
    ax.set_title('Average Stock Level vs Demand', fontsize=12, fontweight='bold')
    ax.set_xlabel('Average Weekly Demand (units)')
    ax.set_ylabel('Average Stock Level (units)')
    return fig

def forecast_vs_actual(df):
    """Chart 6: Forecast vs actual last 8 weeks (top 3 SKUs)."""
    top_3 = df.groupby('sku_id')['revenue'].sum().nlargest(3).index
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, sku in enumerate(top_3):
        sku_data = df[df['sku_id'] == sku].sort_values('week').tail(8)
        ax.plot(range(len(sku_data)), sku_data['units_sold'], marker='o', label=sku)
    ax.set_title('Last 8 Weeks Demand (Top 3 SKUs)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Week')
    ax.set_ylabel('Units Sold')
    ax.legend()
    return fig
