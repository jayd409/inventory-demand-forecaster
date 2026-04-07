import pandas as pd
import numpy as np

def forecast_sku(series, span=4, ahead=8):
    """EWMA forecast for a single SKU's weekly demand."""
    if len(series) < 2:
        return [series.iloc[0]] * ahead
    ewma = series.ewm(span=span, adjust=False).mean()
    last = float(ewma.iloc[-1])
    slope = (ewma.iloc[-1] - ewma.iloc[max(0, len(ewma)-4)]) / min(4, len(ewma))
    return [round(max(0, last + slope*i + np.random.normal(0, last*0.05)), 0) for i in range(1, ahead+1)]

def reorder_report(df):
    """Generate reorder recommendations based on stock coverage."""
    results = []
    for sku, grp in df.groupby('sku_id'):
        ts = grp.sort_values('week')['units_sold']
        fcast = forecast_sku(ts)
        avg_demand = np.mean(fcast)
        current_stock = grp['stock_level'].iloc[-1]
        weeks_cover = current_stock / max(avg_demand, 1)
        results.append({
            'sku_id': sku,
            'product': grp['product_name'].iloc[0],
            'category': grp['category'].iloc[0],
            'current_stock': int(current_stock),
            'forecast_8wk_avg': round(avg_demand, 0),
            'weeks_coverage': round(weeks_cover, 1),
            'reorder_needed': weeks_cover < 3,
        })
    return pd.DataFrame(results).sort_values('weeks_coverage')
