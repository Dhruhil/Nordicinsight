# Data notes

## Prices
- Source: ENTSO-E day-ahead prices, SE3 and SE4
- Convert to UTC, average to hourly, interpolate at most 3 missing hours

## Weather
- Source: SMHI station 97400 (Stockholm-Arlanda), parameter 1 (air temperature)
- Archive and latest-months joined, duplicates removed (newest kept)
- Period: 2023-01-01 to 2026-10-26, hourly, UTC
- 62 missing hours (about 0.2%), to be interpolated
- Limitation: one station used as a proxy for both SE3 and SE4