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

- Weather values checked: range -21.6 to 29.9 °C, no sentinel values

- Weather gaps: 41 stretches, median 1 hour, longest 5 hours.
- Fill rule: linear interpolation up to 3 hours, then forward-fill up to 6 hours.