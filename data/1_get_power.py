"""NASA POWER daily point API -> power_daily.csv   (no login needed)
Source: NASA POWER, AG community. Meteorology = MERRA-2, 0.5 deg lat x 0.625 deg lon,
daily from 1981-01-01. ALLSKY_SFC_SW_DWN = CERES/SRB, 1 x 1 deg (starts later than 1981).
pip install requests pandas"""
import sys, json, datetime as dt
import requests, pandas as pd
from config import LAT, LON

PARAMS = "T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,WS2M,ALLSKY_SFC_SW_DWN"
BASE = "https://power.larc.nasa.gov/api/temporal/daily/point"

def fetch(end):
    q = dict(parameters=PARAMS, community="AG", longitude=LON, latitude=LAT,
             start="19810101", end=end.strftime("%Y%m%d"), format="JSON")
    r = requests.get(BASE, params=q, timeout=300)
    print(r.url, "->", r.status_code)
    return r

end = dt.date.today()
for back in (0, 3, 7, 14):                 # POWER lags a few days; step back if refused
    r = fetch(end - dt.timedelta(days=back))
    if r.ok:
        break
else:
    sys.exit("POWER refused the request:\n" + r.text[:1000])

js = r.json()
json.dump({k: js.get(k) for k in ("geometry", "header", "parameters")},
          open("power_meta.json", "w"), indent=1)
fill = js.get("header", {}).get("fill_value", -999)
df = pd.DataFrame(js["properties"]["parameter"])
df.index = pd.to_datetime(df.index, format="%Y%m%d")
df.index.name = "date"
df = df.mask(df == fill)                    # -999 -> empty cell, never a fake number
df.to_csv("power_daily.csv")
print("saved power_daily.csv", df.shape, df.index.min().date(), "->", df.index.max().date())
print("grid-cell centre + elevation used by POWER:", js.get("geometry", {}).get("coordinates"))
print("first/last valid day per parameter:")
for c in df:
    v = df[c].dropna()
    print(f"  {c:18s} {v.index.min().date()} -> {v.index.max().date()}  missing days: {df[c].isna().sum()}")
