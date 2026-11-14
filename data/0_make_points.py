"""Writes appeears_points.csv for the AppEEARS point request.
  - 'center' + N/S/E/W 90 m away  -> SRTM slope (one point has no slope)
  - m_r_c: a 3x3 grid ~240 m apart -> MODIS NDVI averaged over 9 pixels, so one odd pixel
    (a road, a greenhouse, an olive grove) does not decide the result.
Merged from Mahmoud's (slope points) and Tia's (3x3 MODIS block) versions."""
import math, csv
from config import LAT, LON

def points():
    pts = []
    d = 90.0
    dlat = d / 111_320.0
    dlon = d / (111_320.0 * math.cos(math.radians(LAT)))
    for i, la, lo in [("center", LAT, LON), ("N", LAT + dlat, LON), ("S", LAT - dlat, LON),
                      ("E", LAT, LON + dlon), ("W", LAT, LON - dlon)]:
        pts.append((i, "srtm", la, lo))
    g = 240.0
    glat = g / 110_574.0
    glon = g / (111_320.0 * math.cos(math.radians(LAT)))
    for r in (-1, 0, 1):
        for c in (-1, 0, 1):
            pts.append((f"m_{r}_{c}", "modis", LAT + r * glat, LON + c * glon))
    return pts

if __name__ == "__main__":
    with open("appeears_points.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Category", "Latitude", "Longitude"])
        for i, cat, la, lo in points():
            w.writerow([i, cat, f"{la:.6f}", f"{lo:.6f}"])
    print("wrote appeears_points.csv with", len(points()), "points")
