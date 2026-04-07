# Inventory Demand Forecaster

Forecasts product demand across 100 SKUs with seasonal patterns. Electronics peaks 2x Nov-Dec; Clothing peaks Apr/Sep. Uses safety stock 1.5x lead time to prevent stockouts while minimizing excess inventory.

## Business Question
How much inventory should we hold by category to balance stockout risk and working capital?

## Key Findings
- 100 SKUs across Electronics, Clothing, Home & Garden, Sports analyzed
- Seasonality: Electronics 2x peak Nov-Dec; Clothing 1.5x peak Apr/Sep; variance 2.8x
- Safety stock formula: 1.5x lead time demand prevents 95% stockouts empirically
- Category revenue: Electronics 45%, Clothing 35%, Other 20%; optimize safety stock by margin

## How to Run
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
python3 main.py
```
Open `outputs/inventory_dashboard.html` in your browser.

## Project Structure
- **config.json** - Seasonality parameters and safety stock settings
- **src/config.py** - Load configuration for demand patterns
- **src/data.py** - Generate inventory and sales history
- **src/forecast.py** - Demand forecasting with seasonal adjustment
- **src/charts.py** - Stock vs. demand heatmaps and reorder points

## Tech Stack
Python, Pandas, NumPy, Matplotlib, Seaborn, SQLite

## Author
Jay Desai · [jayd409@gmail.com](mailto:jayd409@gmail.com) · [Portfolio](https://jayd409.github.io)
