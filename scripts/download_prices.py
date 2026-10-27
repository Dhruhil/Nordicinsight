import os

import pandas as pd
from dotenv import load_dotenv
from entsoe import EntsoePandasClient

load_dotenv()
client = EntsoePandasClient(api_key=os.environ["ENTSOE_API_KEY"])

start = pd.Timestamp("2023-01-01", tz="Europe/Stockholm")
end = pd.Timestamp.now(tz="Europe/Stockholm").normalize()

for zone in ["SE_3", "SE_4"]:
    s = client.query_day_ahead_prices(zone, start=start, end=end)
    s.rename("price_eur_mwh").to_frame().to_parquet(f"data/raw/prices_{zone}.parquet")
    print(zone, len(s), s.index.min(), s.index.max())