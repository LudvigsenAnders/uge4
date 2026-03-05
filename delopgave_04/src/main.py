import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

path = Path(__file__).resolve().parents[2]
print(path)

path_housing = path / "data" / "DKHousingPricesSample100k.csv"

path_out = path / "data" / "csv_output"

df = pd.read_csv(
    path_housing,
    sep=",",
    header=0,
    index_col=False,
    on_bad_lines='warn',
    dtype={
        "date": "string",
        "quarter": "string",
        "house_id": "int64",
        "house_type": "string",
        "sales_type": "string",
        "year_build": "int64",
        "purchase_price": "float64",
        "%_change_between_offer_and_purchase": "float64",
        "no_rooms": "int64",
        "sqm": "float64",
        "sqm_price": "float64",
        "address": "string",
        "zip_code": "int64",
        "city": "string",
        "area": "string",
        "region": "string",
        "%_nom_interest_rate%": float,
        "%_dk_ann_infl_rate%": float,
        "%_yield_on_mortgage_credit_bonds%": float
    }
)

df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%Y-%m-%d').dt.date
df['quarter'] = pd.PeriodIndex(df['quarter'], freq='Q')
print(df.head(10))

df_region_grp = df.groupby('region')['purchase_price'].agg(['mean', 'median', 'std', 'min', 'max'])
print(df_region_grp)

df_house_type_grp = df.groupby('house_type')['purchase_price'].agg(['mean', 'median', 'std', 'min', 'max'])
print(df_house_type_grp)

df_house_type_grp.plot(kind='bar', y='mean', title='Average Purchase Price by House Type')
plt.show()
