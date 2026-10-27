import pandas as pd


def load_hourly_prices(zone: str) -> pd.Series:
    df = pd.read_parquet(f"data/raw/prices_{zone}.parquet")
    s = df["price_eur_mwh"].tz_convert("UTC").resample("1h").mean()
    s = s[s.index <= pd.Timestamp.now(tz="UTC").floor("1h")]
    print(f"{zone}: {len(s)} hours, {int(s.isna().sum())} missing")
    return s.interpolate(limit=3)


def load_hourly_weather(station: int = 97400) -> pd.Series:
    temp = pd.read_parquet(f"data/raw/weather_{station}.parquet")["temp_c"]
    # Fill short gaps: interpolate up to 3 hours, then forward-fill up to 6 hours
    return temp.interpolate(limit=3).ffill(limit=6)