import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_inventory(weeks=104):
    """Generate 2 years of weekly retail inventory data with realistic product names and pricing.

    Categories: Electronics, Clothing, Food & Beverage, Health, Home
    Seasonal patterns:
    - Electronics: Peak Nov-Dec (holiday shopping)
    - Clothing: Peaks Apr and Sep (spring/fall)
    - Food & Beverage: Year-round with holiday bumps
    """
    rng = np.random.default_rng(seed=42)

    # Real product names organized by category
    products = {
        'Electronics': [
            ('ELEC-001', 'Laptop 15inch', 899),
            ('ELEC-002', 'Wireless Mouse', 29),
            ('ELEC-003', 'USB-C Hub', 49),
            ('ELEC-004', 'Bluetooth Headphones', 79),
            ('ELEC-005', 'Phone Case (iPhone)', 19),
        ],
        'Clothing': [
            ('CLTH-001', 'Cotton T-Shirt', 24),
            ('CLTH-002', 'Denim Jeans', 79),
            ('CLTH-003', 'Winter Jacket', 149),
            ('CLTH-004', 'Athletic Sneakers', 119),
            ('CLTH-005', 'Wool Sweater', 89),
        ],
        'Food & Beverage': [
            ('FOOD-001', 'Ground Coffee Beans (1lb)', 12),
            ('FOOD-002', 'Protein Bar (Box of 12)', 19),
            ('FOOD-003', 'Sports Drink (6-pack)', 8),
            ('FOOD-004', 'Granola Mix (Bulk)', 14),
            ('FOOD-005', 'Vitamin Supplement', 22),
        ],
        'Health': [
            ('HLTH-001', 'Multivitamin (Bottle)', 15),
            ('HLTH-002', 'Sunscreen SPF 50', 18),
            ('HLTH-003', 'Hand Sanitizer', 6),
            ('HLTH-004', 'Face Masks (50-pack)', 12),
            ('HLTH-005', 'Thermometer', 25),
        ],
        'Home': [
            ('HOME-001', 'LED Desk Lamp', 45),
            ('HOME-002', 'Plastic Storage Box', 16),
            ('HOME-003', 'Door Mat', 22),
            ('HOME-004', 'Pillow Case (2-pack)', 19),
            ('HOME-005', 'Shower Curtain', 28),
        ]
    }

    sku_data = []

    for category, items in products.items():
        for sku_id, product_name, unit_price in items:
            # Base demand by category and SKU
            if category == 'Electronics':
                base_demand = rng.normal(45, 12)
            elif category == 'Clothing':
                base_demand = rng.normal(60, 15)
            elif category == 'Food & Beverage':
                base_demand = rng.normal(80, 20)
            elif category == 'Health':
                base_demand = rng.normal(50, 12)
            else:  # Home
                base_demand = rng.normal(55, 14)

            # Lead time realistic values (days)
            if category == 'Electronics':
                lead_time = rng.integers(7, 15)
            elif category == 'Food & Beverage':
                lead_time = rng.integers(3, 8)
            else:
                lead_time = rng.integers(5, 12)

            for week in range(weeks):
                date = datetime(2022, 1, 1) + timedelta(weeks=week)
                month = date.month

                # Realistic seasonal patterns
                if category == 'Electronics':
                    # Black Friday/Cyber Monday, Holiday shopping
                    seasonal = 2.0 if month in [11, 12] else 0.7 if month in [7, 8] else 1.0
                elif category == 'Clothing':
                    # Spring and Fall seasons
                    seasonal = 1.5 if month in [3, 4, 9, 10] else 0.8 if month in [7, 8] else 1.0
                elif category == 'Food & Beverage':
                    # Year-round with holiday bumps
                    seasonal = 1.4 if month in [11, 12] else 0.9 if month in [6, 7] else 1.0
                elif category == 'Health':
                    # Seasonal: higher in cold months, summer (sunscreen)
                    seasonal = 1.3 if month in [1, 2, 6, 7, 12] else 0.9
                else:  # Home
                    # Spring cleaning, holiday prep
                    seasonal = 1.4 if month in [3, 4, 11] else 0.8 if month in [7, 8] else 1.0

                # Weekly demand with realistic variation
                weekly_demand = base_demand * seasonal + rng.normal(0, base_demand * 0.15)
                units_sold = int(max(2, weekly_demand))

                # Stock level management
                # Safety stock = 1.5 * lead_time * average_demand
                avg_demand = base_demand * seasonal
                safety_stock = max(15, int(1.5 * (lead_time / 7) * avg_demand))
                stock_level = safety_stock + rng.normal(0, safety_stock * 0.2)
                stock_level = int(max(5, stock_level))

                revenue = units_sold * unit_price

                sku_data.append({
                    'sku_id': sku_id,
                    'product_name': product_name,
                    'category': category,
                    'week': week,
                    'date': date.strftime('%Y-%m-%d'),
                    'units_sold': units_sold,
                    'price': unit_price,
                    'revenue': revenue,
                    'stock_level': stock_level,
                    'lead_time_days': lead_time,
                })

    return pd.DataFrame(sku_data)
