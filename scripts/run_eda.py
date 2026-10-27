import matplotlib

matplotlib.use("Agg")  # no screen inside Docker, so save to files only
import matplotlib.pyplot as plt
import pandas as pd

from nordicinsight.data import load_hourly_prices, load_hourly_weather

OUT = "docs/figures"

for zone in ["SE_3", "SE_4"]:
    price = load_hourly_prices(zone).dropna()
    # Local time makes hour-of-day and weekday patterns easier to read.
    local = price.tz_convert("Europe/Stockholm")

    # 1. Average price by hour of day and by weekday
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    local.groupby(local.index.hour).mean().plot(ax=ax[0], marker="o")
    ax[0].set(title=f"{zone}: mean price by hour of day", xlabel="hour", ylabel="EUR/MWh")
    local.groupby(local.index.day_of_week).mean().plot(ax=ax[1], marker="o")
    ax[1].set(title=f"{zone}: mean price by weekday (0=Mon)", xlabel="weekday")
    fig.tight_layout()
    fig.savefig(f"{OUT}/{zone}_hour_weekday.png", dpi=120)
    plt.close(fig)

    # 2. Price over time, spikes marked (above the 99th percentile)
    thr = price.quantile(0.99)
    fig, ax = plt.subplots(figsize=(12, 4))
    price.plot(ax=ax, linewidth=0.5)
    price[price > thr].plot(ax=ax, style="r.", markersize=3)
    ax.set(title=f"{zone}: price, spikes above {thr:.0f} EUR/MWh in red", ylabel="EUR/MWh")
    fig.tight_layout()
    fig.savefig(f"{OUT}/{zone}_spikes.png", dpi=120)
    plt.close(fig)

    # 3. Price vs temperature
    temp = load_hourly_weather()
    df = pd.concat([price.rename("price"), temp.rename("temp")], axis=1).dropna()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(df["temp"], df["price"], s=2, alpha=0.2)
    ax.set(title=f"{zone}: price vs temperature", xlabel="temp C", ylabel="EUR/MWh")
    fig.tight_layout()
    fig.savefig(f"{OUT}/{zone}_price_vs_temp.png", dpi=120)
    plt.close(fig)

    # Numbers to quote in the findings
    print(f"\n{zone}")
    print("price/temp correlation:", round(df["price"].corr(df["temp"]), 3))
    print("share of negative-price hours:", round((price < 0).mean(), 3))
    print("99th percentile:", round(thr, 1))
    print("mean by year:\n", price.groupby(price.index.year).mean().round(1))