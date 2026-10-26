import io

import httpx
import pandas as pd

STATION = 97400
BASE = (
    "https://opendata-download-metobs.smhi.se/api/version/latest/"
    f"parameter/1/station/{STATION}"
)


def fetch_archive() -> pd.Series:
    r = httpx.get(f"{BASE}/period/corrected-archive/data.csv", timeout=60)
    r.raise_for_status()
    lines = r.text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("Datum"))
    df = pd.read_csv(io.StringIO("\n".join(lines[start:])), sep=";", usecols=[0, 1, 2])
    df.columns = ["date", "time", "temp_c"]
    df["ts"] = pd.to_datetime(df["date"] + " " + df["time"], utc=True)
    return df.set_index("ts")["temp_c"].astype(float)


def fetch_latest() -> pd.Series:
    r = httpx.get(f"{BASE}/period/latest-months/data.json", timeout=60)
    r.raise_for_status()
    rows = r.json()["value"]
    idx = pd.to_datetime([x["date"] for x in rows], unit="ms", utc=True)
    return pd.Series([float(x["value"]) for x in rows], index=idx)


archive = fetch_archive()
latest = fetch_latest()
print("archive:", archive.index.min(), "->", archive.index.max())
print("latest: ", latest.index.min(), "->", latest.index.max())

temp = pd.concat([archive, latest])
temp = temp[~temp.index.duplicated(keep="last")].sort_index()
temp = temp[temp.index >= "2023-01-01"]
temp = temp.resample("1h").mean()
print("hours:", len(temp), "missing:", int(temp.isna().sum()))

temp.rename("temp_c").to_frame().to_parquet(f"data/raw/weather_{STATION}.parquet")
print("saved data/raw/weather_97400.parquet")