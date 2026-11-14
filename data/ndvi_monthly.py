"""Read-only seasonal NDVI check: does the 3x3 MODIS block look rainfed (green Feb-Apr, low in summer)
or irrigated (green in summer)? Reads *MOD13Q1-061-results.csv (AppEEARS), never touches ardi_data.json.
Keeps Category == "modis" rows (the 3x3 block) with pixel_reliability 0 (good) or 1 (marginal),
same scaling and fill handling as 3_indicators.py. Month = month of the composite's start date.
Writes ndvi_monthly.csv: month, mean_ndvi (all years, all 9 pixels), n_composites (distinct 16-day dates),
n_pixel_values (pixel x composite values averaged). Prints the mean Jul-Sep NDVI per pixel ID.
Usage (from the ardi_data folder):  python ndvi_monthly.py"""
import glob, sys
import numpy as np, pandas as pd

f = sorted(glob.glob("*MOD13Q1-061-results.csv"))
if not f:
    sys.exit("no *MOD13Q1-061-results.csv in this folder")
m = pd.read_csv(f[0])
c_ndvi = [c for c in m.columns if c.endswith("NDVI")][0]
c_rel = [c for c in m.columns if c.endswith("pixel_reliability") and "Description" not in c][0]
m = m[m["Category"].astype(str) == "modis"].copy()
m["Date"] = pd.to_datetime(m["Date"])
v = pd.to_numeric(m[c_ndvi], errors="coerce")
if v.abs().max() > 1.5:
    v = v * 0.0001                              # unscaled integers -> NDVI
v[(v < -0.2) | (v > 1.0)] = np.nan              # fill values
rel = pd.to_numeric(m[c_rel], errors="coerce")
v[~rel.isin([0, 1])] = np.nan                   # keep good (0) + marginal (1)
m["ndvi"] = v
m = m.dropna(subset=["ndvi"])
m["month"] = m["Date"].dt.month

print(f"source: {f[0]}; pixels: {m['ID'].nunique()}; usable pixel values: {len(m)}; "
      f"dates {m['Date'].min().date()} to {m['Date'].max().date()}")
mon = m.groupby("month").agg(mean_ndvi=("ndvi", "mean"), n_composites=("Date", "nunique"),
                             n_pixel_values=("ndvi", "size")).reset_index()
mon["mean_ndvi"] = mon["mean_ndvi"].round(3)
mon.to_csv("ndvi_monthly.csv", index=False)
print("\nndvi_monthly.csv")
print(mon.to_string(index=False))

summer = m[m["month"].isin([7, 8, 9])].groupby("ID")["ndvi"].agg(["mean", "size"]).round(3)
summer.columns = ["mean_ndvi_JulSep", "n_values"]
print("\nMean Jul-Sep NDVI per pixel ID")
print(summer.to_string())
