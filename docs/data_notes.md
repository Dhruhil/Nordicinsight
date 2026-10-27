# Data notes

## Prices
- Source: ENTSO-E Transparency Platform, day-ahead prices, zones SE_3 and SE_4
- Downloaded: 2026-10-27 via `scripts/download_prices.py` (range 2023-01-01 to 2026-10-27)
- Resolution: hourly until 2025-09-30, 15-minute from 2025-10-01
- Processing: convert to UTC, average to hourly, drop hours after "now" (not yet observed),
  interpolate gaps of at most 3 hours
- Result: 33,481 hourly rows, 2 missing hours (before interpolation)
- Value range (SE_3): -60.04 to 707.52 EUR/MWh, mean about 50. Negative prices are real, not errors.
- Known quirks: two 2-hour gaps and one 30-minute step in the raw data

## Weather
- Source: SMHI Open Data, station 97400 (Stockholm-Arlanda), parameter 1 (air temperature)
- Archive and latest-months joined, duplicate timestamps removed (newest kept)
- Period: 2023-01-01 to 2026-10-26, hourly, UTC
- Value range: -21.6 to 29.9 °C, no sentinel values (such as 9999)
- Gaps: 62 missing hours (about 0.2%) in 41 stretches, median 1 hour, longest 5 hours
- Fill rule: linear interpolation up to 3 hours, then forward-fill up to 6 hours
- Limitation: one Stockholm station is used as a proxy for both SE_3 and SE_4

## Open issues
- SE_4 (southern Sweden) weather is not well represented by a Stockholm station.
  Consider adding a southern station (for example Malmö) in Phase 2.