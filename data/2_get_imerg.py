"""IMERG V07 Final Daily (GPM_3IMERGDF.07) point time series -> imerg_daily.csv
Service: GES DISC "Giovanni in the Cloud: Time Series" API (single point only).
Needs a free Earthdata Login token:
  https://urs.earthdata.nasa.gov  ->  log in  ->  "Generate Token"  ->  copy it, then
  Linux:  export EARTHDATA_TOKEN='paste-token-here'
(or: pip install earthaccess   and the script will ask for your username/password)
pip install requests pandas"""
import os, re, sys, time
import requests, pandas as pd
from config import LAT, LON

URL = "https://api.giovanni.earthdata.nasa.gov/timeseries"
DATA = "GPM_3IMERGDF_07_precipitation"       # mm/day, 0.1 deg, UTC days
START_YEAR, END = 1998, "2025-09-30"         # V07 Final record: 1998-01-01 .. 2025-09-30

token = os.environ.get("EARTHDATA_TOKEN")
if not token:
    try:
        import earthaccess
        earthaccess.login()
        token = earthaccess.get_edl_token()["access_token"]
    except Exception as e:
        sys.exit(f"No EARTHDATA_TOKEN set and earthaccess login failed: {e}")
hdr = {"Authorization": f"Bearer {token}"}

ROW = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})[T ]?[\d:]*Z?\s*,\s*(-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*$")
rows, raw = [], []
for y0 in range(START_YEAR, 2026, 4):        # 4-year chunks keep each request small
    t0 = f"{y0}-01-01T00:00:00"
    t1 = min(f"{y0 + 3}-12-31", END) + "T23:59:59"
    q = {"data": DATA, "location": f"[{LAT},{LON}]", "time": f"{t0}/{t1}"}
    for attempt in range(3):
        r = requests.get(URL, params=q, headers=hdr, timeout=600)
        if r.ok and r.text.strip():
            break
        print("  retry", attempt + 1, r.status_code, r.text[:200]); time.sleep(10)
    else:
        sys.exit(f"Giovanni API failed for {t0}/{t1}: HTTP {r.status_code}\n{r.text[:500]}\n"
                 "Use the Giovanni web steps instead (see the export, section 2b-B).")
    raw.append(r.text)
    n0 = len(rows)
    for line in r.text.splitlines():
        m = ROW.match(line)
        if m:
            rows.append((m.group(1), float(m.group(2))))
    print(f"{t0[:10]} .. {t1[:10]}: {len(rows) - n0} days")

open("imerg_raw.txt", "w").write("\n=====\n".join(raw))   # keep the untouched response
if not rows:
    sys.exit("Got a response but could not find 'date,value' rows. Open imerg_raw.txt and check.")
df = pd.DataFrame(rows, columns=["date", "precip_mm"]).drop_duplicates("date")
df.loc[df.precip_mm < 0, "precip_mm"] = float("nan")       # fill values -> empty
df.to_csv("imerg_daily.csv", index=False)
print("saved imerg_daily.csv:", len(df), "days", df.date.min(), "->", df.date.max())
print("header lines of the raw response (check lat/lon of the grid cell used):")
print("\n".join(raw[0].splitlines()[:12]))
