"""Optional: submit / check / download the AppEEARS request by script instead of the website.
(Adapted from Tia's version.)  Needs a free Earthdata Login.
  python 0b_appeears_submit.py submit     -> do this FIRST, it queues
  python 0b_appeears_submit.py status
  python 0b_appeears_submit.py download   -> saves the *-results.csv files here
If anything fails, use the website steps in README.md instead. Do not lose time on it."""
import datetime as dt, getpass, json, sys
import requests
from config import POINT_NAME
from importlib import import_module
points = import_module("0_make_points").points

API = "https://appeears.earthdatacloud.nasa.gov/api/"
TASK = "appeears_task.json"

def login():
    u = input("Earthdata username: "); p = getpass.getpass("Earthdata password: ")
    r = requests.post(API + "login", auth=(u, p)); r.raise_for_status()
    return {"Authorization": "Bearer " + r.json()["token"]}

def submit():
    h = login()
    task = {"task_type": "point", "task_name": f"ardi_{POINT_NAME}",
            "params": {"dates": [{"startDate": "02-18-2000", "endDate": dt.date.today().strftime("%m-%d-%Y")}],
                       "layers": [{"product": "MOD13Q1.061", "layer": "_250m_16_days_NDVI"},
                                  {"product": "MOD13Q1.061", "layer": "_250m_16_days_pixel_reliability"},
                                  {"product": "SRTMGL1_NC.003", "layer": "SRTMGL1_DEM"}],
                       "coordinates": [{"id": i, "category": c, "latitude": round(la, 6), "longitude": round(lo, 6)}
                                       for i, c, la, lo in points()]}}
    r = requests.post(API + "task", json=task, headers=h); print(r.status_code, r.text[:300]); r.raise_for_status()
    json.dump({"task_id": r.json()["task_id"]}, open(TASK, "w")); print("submitted, task id saved to", TASK)

def status(h=None):
    h = h or login(); tid = json.load(open(TASK))["task_id"]
    s = requests.get(API + f"task/{tid}", headers=h).json(); print("status:", s.get("status"), s.get("progress", ""))
    return s.get("status"), h, tid

def download():
    st, h, tid = status()
    if st != "done":
        return print("not finished yet")
    for f in requests.get(API + f"bundle/{tid}", headers=h).json()["files"]:
        if f["file_name"].endswith(".csv"):
            r = requests.get(API + f"bundle/{tid}/{f['file_id']}", headers=h, stream=True); r.raise_for_status()
            name = f["file_name"].split("/")[-1]
            with open(name, "wb") as fh:
                for ch in r.iter_content(1 << 16): fh.write(ch)
            print("saved", name)

if __name__ == "__main__":
    {"submit": submit, "status": status, "download": download}[sys.argv[1] if len(sys.argv) > 1 else "submit"]()
