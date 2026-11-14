# Ardi data folder (Group C: Mahmoud + Rana) — merged from Mahmoud's and Tia's versions, tested on synthetic data

Order tonight:
1. Check the point on a satellite map: inside the West Bank, open RAINFED field crops, no buildings,
   greenhouses or olives within ~250 m. Edit LAT/LON in config.py.
2. `python 0_make_points.py`  -> appeears_points.csv (center + N/S/E/W for slope, 3x3 grid for NDVI)
3. AppEEARS FIRST (it queues): website Extract -> Point, upload appeears_points.csv, 02-18-2000 -> today,
   layers MOD13Q1.061 `_250m_16_days_NDVI` + `_250m_16_days_pixel_reliability`, SRTMGL1_NC.003 `SRTMGL1_DEM`.
   (or `python 0b_appeears_submit.py submit` / `status` / `download`)
4. `python 1_get_power.py`  (no login)
5. `python 2_get_imerg.py` with EARTHDATA_TOKEN set; if it fails within 10 min, use Giovanni in the browser
   (Time Series Area-Averaged, GPM_3IMERGDF v07 precipitation, 1998-01-01 to 2025-09-30, small box around the point),
   save the CSV as imerg_daily.csv.
6. `python 3_indicators.py` -> ardi_summary.md + **ardi_data.json** (send this file to Group A immediately).
   Re-run when AppEEARS finishes; send the new ardi_data.json again.
IMERG V07 Final ends Sep 2025 -> 27 complete seasons (1998/99-2024/25). Say "5th-driest of 27 seasons".
Run scripts from inside this folder (`python 3_indicators.py`), so they find config.py.
