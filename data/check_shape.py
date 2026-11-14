"""Checks that ardi_data.json and crops.json still have the contract shape (DATA_CONTRACT.md v1).
It checks KEYS and TYPES only, never values.   Usage (from the ardi_data folder):
    python check_shape.py                 -> checks ardi_data.json and crops.json
    python check_shape.py ardi_data.json  -> checks one file
Exit code 0 = shape OK, 1 = problem (each problem is printed)."""
import json, sys, os

NUM = (int, float)
errs = []
def err(m): errs.append(m)
def keys_exact(obj, want, where):
    if not isinstance(obj, dict): return err(f"{where}: should be an object, is {type(obj).__name__}")
    extra, miss = set(obj) - set(want), set(want) - set(obj)
    if extra: err(f"{where}: unexpected keys {sorted(extra)}")
    if miss: err(f"{where}: missing keys {sorted(miss)}")
def typ(v, types, where, nullable=True):
    if v is None:
        if not nullable: err(f"{where}: must not be null")
        return
    if isinstance(v, bool) and bool not in (types if isinstance(types, tuple) else (types,)):
        return err(f"{where}: is true/false, expected {types}")
    if not isinstance(v, types): err(f"{where}: is {type(v).__name__}, expected {types}")

def check_ardi(d):
    keys_exact(d, ["contract_version", "placeholder", "generated", "point", "datasets", "seasons",
                   "dry_line", "slope", "backtest"], "ardi_data")
    if d.get("contract_version") != 1: err("contract_version must be 1")
    typ(d.get("placeholder"), bool, "placeholder", False)
    typ(d.get("generated"), str, "generated")
    p = d.get("point") or {}
    keys_exact(p, ["name", "lat", "lon"], "point")
    for k in ("lat", "lon"): typ(p.get(k), NUM, f"point.{k}")
    ds = d.get("datasets")
    if not isinstance(ds, list): err("datasets must be a list")
    else:
        for i, x in enumerate(ds):
            keys_exact(x, ["id", "label", "role"], f"datasets[{i}]")
            if x.get("id") not in ("imerg", "power", "modis", "srtm"): err(f"datasets[{i}].id must be imerg|power|modis|srtm")
    req = ["season", "rain_mm", "rank_driest", "days_ge20mm", "dry_spells_10d_jfm", "longest_dry_run_jfm"]
    opt = ["heat_days_mam", "frost_days", "bare_months", "ndvi_peak"]
    ss = d.get("seasons")
    if not isinstance(ss, list): err("seasons must be a list")
    else:
        names = []
        for i, s in enumerate(ss):
            if not isinstance(s, dict): err(f"seasons[{i}] must be an object"); continue
            extra = set(s) - set(req + opt); miss = set(req) - set(s)
            if extra: err(f"seasons[{i}]: unexpected keys {sorted(extra)}")
            if miss: err(f"seasons[{i}]: missing keys {sorted(miss)}")
            typ(s.get("season"), str, f"seasons[{i}].season")
            for k in req[1:] + opt:
                if k in s: typ(s[k], NUM, f"seasons[{i}].{k}")
            names.append(s.get("season") or "")
        if names != sorted(names): err("seasons must be oldest first")
    dl = d.get("dry_line")
    if dl is not None:
        keys_exact(dl, ["season", "rain_mm", "rank", "n_seasons", "pct_of_mean", "mean_rain_mm"], "dry_line")
        for k in ("rain_mm", "rank", "n_seasons", "pct_of_mean", "mean_rain_mm"): typ(dl.get(k), NUM, f"dry_line.{k}")
    sl = d.get("slope")
    if sl is not None:
        keys_exact(sl, ["slope_pct", "elevation_m", "note"], "slope")
        for k in ("slope_pct", "elevation_m"): typ(sl.get(k), NUM, f"slope.{k}")
    bt = d.get("backtest")
    if bt is not None:
        keys_exact(bt, ["n_seasons", "driest_below_mean", "driest_below_1sd", "spearman_rain_vs_ndvi", "rows"], "backtest")
        for i, r in enumerate(bt.get("rows") or []):
            keys_exact(r, ["season", "rain_mm", "rank", "ndvi_peak", "anomaly_sd"], f"backtest.rows[{i}]")

def check_crops(c):
    keys_exact(c, ["contract_version", "status_values", "crops", "rotations", "horizon_seasons"], "crops.json")
    ck = ["id", "name_en", "name_ar", "family", "legume", "min_season_rain_mm", "stage_risk",
          "bare_months_typical", "yield_t_ha", "price_ils_t", "status", "sources"]
    ids = set()
    for i, x in enumerate(c.get("crops") or []):
        keys_exact(x, ck, f"crops[{i}]"); ids.add(x.get("id"))
        if x.get("family") not in ("cereal", "legume"): err(f"crops[{i}].family must be cereal|legume")
        typ(x.get("legume"), bool, f"crops[{i}].legume", False)
        for k in ("min_season_rain_mm", "bare_months_typical", "yield_t_ha", "price_ils_t"): typ(x.get(k), NUM, f"crops[{i}].{k}")
        keys_exact(x.get("stage_risk") or {}, ["heat_mam", "dry_jfm"], f"crops[{i}].stage_risk")
        if x.get("status") not in ("sourced", "local", "illustrative", "todo"): err(f"crops[{i}].status invalid")
        if not isinstance(x.get("sources"), list): err(f"crops[{i}].sources must be a list")
    rk = ["id", "label_en", "label_ar", "is_current", "status", "note", "cycle"]
    for i, r in enumerate(c.get("rotations") or []):
        extra = set(r) - set(rk + ["card_ar", "card_en"]); miss = set(rk) - set(r)
        if extra: err(f"rotations[{i}]: unexpected keys {sorted(extra)}")
        if miss: err(f"rotations[{i}]: missing keys {sorted(miss)}")
        bad = [x for x in r.get("cycle") or [] if x not in ids]
        if bad: err(f"rotations[{i}].cycle uses unknown crop ids {bad}")
    typ(c.get("horizon_seasons"), int, "horizon_seasons", False)

files = sys.argv[1:] or [f for f in ("ardi_data.json", "crops.json") if os.path.exists(f)]
if not files: sys.exit("no ardi_data.json or crops.json here")
for f in files:
    errs.clear()
    d = json.load(open(f, encoding="utf-8"))
    (check_crops if "crops" in os.path.basename(f) else check_ardi)(d)
    print(f"{f}: " + ("SHAPE OK" if not errs else f"{len(errs)} PROBLEM(S)"))
    for e in errs: print("  -", e)
    if errs: bad = True
sys.exit(1 if "bad" in globals() else 0)
