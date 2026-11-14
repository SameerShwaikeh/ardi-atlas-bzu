# Ardi · facts.md (Group C -> Group B)
Every value below is copied from ardi_summary.md / ardi_data.json / power_meta.json. Missing values say "no data yet".
Generated: 2026-11-14T03:42 · v1 (POWER + IMERG) · Point: jenin_plain, 32.4293, 35.2225 (Jenin plain, West Bank)

Open field-crop strips in the Arraba-Burqin plain (Dothan Valley); rainfed status not confirmed on the ground. Fields are narrow strips, so each satellite value is a mix of several fields.

## 1. Dataset register
| Dataset | Agency | Product / version | Variable (units) | Spatial resolution | Time step | Record used | Access | URL |
|---|---|---|---|---|---|---|---|---|
| IMERG Final | NASA GPM (with JAXA) | GPM_3IMERGDF v07 | precipitation (mm/day) | 0.1 deg (~11 km) | daily | 1998-01-01 to 2025-09-30 from the file; 27 complete Oct-May seasons | Giovanni web (Time Series, Area-Averaged) | https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDF_07/summary |
| POWER | NASA LaRC | POWER daily API, AG community | T2M_MAX, T2M_MIN (deg C); PRECTOTCORR (mm/day) | not stated in power_meta.json | daily | 1981-01-01 to 2026-11-10 | POWER API | https://power.larc.nasa.gov/ |
| MODIS NDVI | NASA LP DAAC | MOD13Q1 v061 | NDVI (unitless) | 250 m (no data yet) | 16-day | no data yet | AppEEARS point request | https://appeears.earthdatacloud.nasa.gov |
| SRTM | NASA / LP DAAC | SRTMGL1_NC v003 | elevation (m) | ~30 m | once, Feb 2000 | no data yet | AppEEARS point request | https://appeears.earthdatacloud.nasa.gov |
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
no data yet (needs the MOD13Q1 AppEEARS results).
Source: MOD13Q1 v061, 250 m. NDVI is a vegetation proxy: it does not identify the crop, the yield or soil health.

## 5. Slope
no data yet (needs the SRTM AppEEARS results). Source: SRTM v3, ~30 m, Feb 2000. Elevation: no data yet.

## 6. Backtest
no data yet (needs the MOD13Q1 AppEEARS results).
If X is low or rho is under about 0.4, say so plainly; do not drop the sentence and do not move the point.

## 7. Say / don't say
- Say "5th-driest of 27 seasons", never "a 1-in-5-year drought forecast".
- Say "the area around the field", never "your field" for IMERG, POWER or MODIS.
- IMERG V07 Final ends 30 Sep 2025; the last season included is 2024/25.

## 8. Still missing
The slides must not mention these:
- ardi_data.json: slope (null), backtest (null), bare_months and ndvi_peak (absent in every season): MODIS + SRTM, waiting for AppEEARS.
- ardi_data.json datasets: modis and srtm not listed yet.
- crops.json, crops wheat, barley, lentil, bitter_vetch: min_season_rain_mm, bare_months_typical, yield_t_ha, price_ils_t are all null (status "todo"; Rana's file).
- crops.json rotations A, B, C: status "illustrative".
