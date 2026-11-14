# Ardi · facts.md (Group C -> Group B)
Every value below is copied from ardi_summary.md / ardi_data.json / power_meta.json / ndvi_monthly.csv. Missing values say "no data yet".
Generated: 2026-11-14T05:16 · v2 (with MODIS + SRTM) · Point: jenin_plain, 32.4293, 35.2225 (Jenin plain, West Bank)

Open field-crop strips in the Arraba-Burqin plain (Dothan Valley); rainfed status not confirmed on the ground. Fields are narrow strips, so each satellite value is a mix of several fields.

## 1. Dataset register
| Dataset | Agency | Product / version | Variable (units) | Spatial resolution | Time step | Record used | Access | URL |
|---|---|---|---|---|---|---|---|---|
| IMERG Final | NASA GPM (with JAXA) | GPM_3IMERGDF v07 | precipitation (mm/day) | 0.1 deg (~11 km) | daily | 1998-01-01 to 2025-09-30 from the file; 27 complete Oct-May seasons | Giovanni web (Time Series, Area-Averaged) | https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDF_07/summary |
| POWER | NASA LaRC | POWER daily API, AG community | T2M_MAX, T2M_MIN (deg C); PRECTOTCORR (mm/day) | not stated in power_meta.json | daily | 1981-01-01 to 2026-11-10 | POWER API | https://power.larc.nasa.gov/ |
| MODIS NDVI | NASA LP DAAC | MOD13Q1 v061 | NDVI (unitless) | 250 m (mean of a 3x3 block of 250 m pixels) | 16-day | 2000-02-18 to 2026-10-16 | AppEEARS point request | https://appeears.earthdatacloud.nasa.gov |
| SRTM | NASA / LP DAAC | SRTMGL1_NC v003 | elevation (m) | ~30 m | once, Feb 2000 | - | AppEEARS point request | https://appeears.earthdatacloud.nasa.gov |
IMERG note: Giovanni limited the area average to the single IMERG cell centred at 35.25E, 32.45N (about 3 km from the point); source: header of imerg_daily.csv.
Not NASA and not used in scores: ERA5, Sentinel-2, GAEZ, SoilGrids. Crop values: see crops.json sources.

## 2. Dry line (stress test, not a forecast)
"The 5th-driest of 27 seasons was 2007/08: 363 mm of Oct-May rain, 77 % of the 27-season mean (473 mm)."
Source: IMERG V07 Final Daily, 0.1 deg, 1998/99-2024/25.

## 3. Heat and frost
- Seasons with at least one day above 32 deg C in Mar-May: 41 of 45.
- Seasons with at least one frost day (below 0 deg C), Oct-May: 0 of 45.
(Counted over all 45 POWER seasons, 1981/82 to 2025/26, as printed in ardi_summary.md.)
Source: NASA POWER (MERRA-2), resolution not stated in power_meta.json. Caveat to keep on the slide: grid-cell average at the cell's mean
elevation, so frost on the plain floor is likely under-counted.

## 4. Bare months
"On average 1.9 months a year had NDVI below 0.2 (range 0-5, 26 years)."
NDVI in Oct-Nov is close to the 0.2 threshold, so the bare-month count is sensitive to that threshold. crops.json uses 6 bare months per crop as an illustrative value; the app does not use the measured number.
(Mean NDVI from ndvi_monthly.csv: October 0.202, November 0.196.)
Source: MOD13Q1 v061, 250 m, mean of a 3x3 block, 2000-02-18 to 2026-10-16. NDVI is a vegetation proxy: it does not identify the crop, the yield or soil health.

## 5. Slope
"2.8 % at the point" (1.6 deg, over a 180 m baseline): not flat. Source: SRTM v3, ~30 m, Feb 2000. Elevation: 231 m.
scoring.js does not use slope.

## 6. Backtest
- Driest 5 seasons with NDVI peak below the mean: 2 of 5.
- Driest 5 seasons with NDVI peak more than 1 SD below the mean: 1 of 5.
- Of the 5 lowest NDVI peaks, how many are among the driest 5 seasons: 1 of 5.
- Spearman rank correlation, season rain vs NDVI peak, all 25 seasons: -0.11.

"In 2 of the 5 driest seasons with MODIS data, the NDVI peak was below normal (Spearman rho = -0.11, 25 seasons)."
The driest IMERG season (1998/99) is before MODIS (Feb 2000), so it is not in the backtest.
Dry-line season 2007/08: NDVI peak anomaly +0.01 (anomaly_sd +0.22).
Peak greenness did not track season rain totals at this point; this is weak evidence and we report it as such.
Rain: IMERG. NDVI: MOD13Q1. Shared seasons: 2000/01-2024/25.

## 7. Seasonal NDVI pattern
Highest mean NDVI: March, 0.585. Lowest mean NDVI: November, 0.196. (ndvi_monthly.csv: all years, all 9 pixels, pixel_reliability 0 or 1.)

## 8. Say / don't say
- Say "5th-driest of 27 seasons", never "a 1-in-5-year drought forecast".
- Say "the area around the field", never "your field" for IMERG, POWER or MODIS.
- IMERG V07 Final ends 30 Sep 2025; the last season included is 2024/25.

## 9. Still missing
The slides must not mention these:
- ardi_data.json: bare_months and ndvi_peak are absent for 1998/99 and 1999/00 (before MODIS starts).
- crops.json, crops wheat, barley, lentil, bitter_vetch: price_ils_t is null, so income is "not scored". All crops and rotations have status "illustrative".
