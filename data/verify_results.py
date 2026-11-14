"""Read-only checks on the real Ardi output files (PART C, C1-C11).
Prints PASS / FAIL / WARN / SKIP per check. It never writes or changes any file.
Usage (from the ardi_data folder):  python verify_results.py"""
import glob, json, math, os, re, subprocess, sys
import pandas as pd

LAT, LON = 32.4293, 35.2225
IMERG_START, IMERG_END = "1998-01-01", "2025-09-30"
EXPECTED_SEASONS = [f"{y}/{str(y + 1)[2:]}" for y in range(1998, 2025)]   # 1998/99 .. 2024/25 = 27
results = []

def rep(cid, status, msg):
    results.append((cid, status, msg))
    print(f"{cid:4s} {status:4s} {msg}")

def isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and not (isinstance(v, float) and math.isnan(v))

def load(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return e

d = load("ardi_data.json")
if isinstance(d, Exception):
    print("cannot read ardi_data.json:", d); sys.exit(1)
seasons = d.get("seasons") or []
N = len(seasons)

# C1 ---------------------------------------------------------------------------
try:
    p = subprocess.run([sys.executable, "check_shape.py", "ardi_data.json", "crops.json"], capture_output=True, text=True)
    ok = all(f"{f}: SHAPE OK" in p.stdout for f in ("ardi_data.json", "crops.json"))
    rep("C1", "PASS" if ok else "FAIL", " / ".join(l for l in p.stdout.splitlines() if l.strip()))
except Exception as e:
    rep("C1", "FAIL", f"check_shape.py did not run: {e}")

# C2 ---------------------------------------------------------------------------
pt = d.get("point") or {}
ok = d.get("placeholder") is False and pt.get("lat") == LAT and pt.get("lon") == LON
rep("C2", "PASS" if ok else "FAIL", f"placeholder={d.get('placeholder')}, lat={pt.get('lat')}, lon={pt.get('lon')}")

# C3 ---------------------------------------------------------------------------
pat = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})[T ]?[\d:]*Z?\s*,\s*(-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)")   # same parser as 3_indicators.py
try:
    rows = [(m.group(1), float(m.group(2))) for m in map(pat.match, open("imerg_daily.csv")) if m]
    s = pd.Series(dict(rows), dtype=float); s.index = pd.to_datetime(s.index); s = s.sort_index()
    s[s < 0] = float("nan")
    full = pd.date_range(IMERG_START, IMERG_END)
    missing = int(s.reindex(full).isna().sum())
    first, last = s.index.min().date(), s.index.max().date()
    ok = str(first) <= IMERG_START and str(last) >= IMERG_END
    rep("C3", ("PASS" if missing == 0 else "WARN") if ok else "FAIL",
        f"imerg_daily.csv {first} -> {last}, {len(s)} rows, missing days in {IMERG_START}..{IMERG_END}: {missing}")
except FileNotFoundError:
    rep("C3", "FAIL", "imerg_daily.csv not found")

# C4 ---------------------------------------------------------------------------
names = [x.get("season") for x in seasons]
miss = [x for x in EXPECTED_SEASONS if x not in names]
extra = [x for x in names if x not in EXPECTED_SEASONS]
if N == 27 and not miss:
    rep("C4", "PASS", f"{N} complete IMERG seasons ({names[0]} to {names[-1]})")
else:
    rep("C4", "WARN", f"{N} seasons; missing {miss} (season dropped if <98 % of its Oct-May days are present); extra {extra}")

# C5 ---------------------------------------------------------------------------
dl = d.get("dry_line") or {}
srt = sorted(seasons, key=lambda x: x["rain_mm"])
fifth = srt[4]["season"] if N >= 5 else None
ok = dl.get("rank") == 5 and dl.get("n_seasons") == N and dl.get("season") == fifth \
     and dl.get("rain_mm") == srt[4]["rain_mm"]
rep("C5", "PASS" if ok else "FAIL",
    f"dry_line {dl.get('season')} {dl.get('rain_mm')} mm rank {dl.get('rank')}/{dl.get('n_seasons')}; "
    f"recomputed 5th-lowest from seasons list: {fifth} ({srt[4]['rain_mm'] if N >= 5 else None} mm)")

# C6 ---------------------------------------------------------------------------
req = ["rain_mm", "rank_driest", "days_ge20mm", "dry_spells_10d_jfm", "longest_dry_run_jfm"]
bad = [(x.get("season"), k) for x in seasons for k in req if not isnum(x.get(k))]
ranks = sorted(x.get("rank_driest") for x in seasons if isnum(x.get("rank_driest")))
rank_ok = ranks == list(range(1, N + 1))
rep("C6", "PASS" if not bad and rank_ok else "FAIL",
    f"non-numeric/NaN fields: {bad or 'none'}; rank_driest is exactly 1..{N}: {rank_ok}")

# C7 ---------------------------------------------------------------------------
try:
    pw = pd.read_csv("power_daily.csv", parse_dates=["date"], index_col="date")
    start = pw.index.min().date()
    last = pw["T2M_MAX"].dropna().index.max().date()
    nohf = [x["season"] for x in seasons if not (isnum(x.get("heat_days_mam")) and isnum(x.get("frost_days")))]
    ok = str(start) == "1981-01-01" and not nohf
    rep("C7", "PASS" if ok else "FAIL",
        f"power_daily.csv starts {start}, last valid T2M_MAX {last}; seasons without heat/frost: {nohf or 'none'}")
except FileNotFoundError:
    rep("C7", "FAIL", "power_daily.csv not found")

# C8 ---------------------------------------------------------------------------
flags = [f"{x['season']} rain_mm={x['rain_mm']}" for x in seasons if isnum(x.get("rain_mm")) and not 150 <= x["rain_mm"] <= 1200]
flags += [f"{x['season']} days_ge20mm={x['days_ge20mm']}" for x in seasons if isnum(x.get("days_ge20mm")) and x["days_ge20mm"] > 60]
flags += [f"{x['season']} frost_days={x['frost_days']}" for x in seasons if isnum(x.get("frost_days")) and x["frost_days"] > 60]
rep("C8", "WARN" if flags else "PASS", f"plausibility flags: {flags or 'none'}")

# C9 ---------------------------------------------------------------------------
mf = sorted(glob.glob("*MOD13Q1-061-results.csv"))
sf = sorted(glob.glob("*SRTMGL1-NC-003-results.csv"))
if not mf and not sf:
    rep("C9", "SKIP", "no AppEEARS results files yet (MODIS/SRTM checks run after AppEEARS)")
else:
    notes, status = [], "PASS"
    if mf:
        m = pd.read_csv(mf[0]); ids = m["ID"].astype(str)
        has = ids.str.startswith("m_").any() or (ids == "center").any()
        cn = [c for c in m.columns if c.endswith("NDVI")]
        v = pd.to_numeric(m[cn[0]], errors="coerce") if cn else pd.Series(dtype=float)
        if len(v) and v.abs().max() > 1.5: v = v * 0.0001
        inr = v[(v >= -0.2) & (v <= 1.0)]
        notes.append(f"MODIS rows for m_*/center: {has}; NDVI values in -0.2..1.0 after scaling: {len(inr)} of {v.notna().sum()}")
        if not has or len(inr) == 0: status = "FAIL"
        mod = next((x for x in d.get("datasets", []) if x.get("id") == "modis"), None)
        if mod: notes.append("modis label: " + mod["label"])
        if os.path.exists("ardi_summary.md"):
            u = re.search(r"(\d+) usable composites of (\d+)", open("ardi_summary.md").read())
            if u: notes.append(f"usable composites: {u.group(1)} of {u.group(2)}")
        if os.path.exists("bare_months.csv"):
            b = pd.read_csv("bare_months.csv")["bare_months"]
            if len(b) and (b.eq(0).all() or b.eq(12).all()):
                status = "WARN" if status == "PASS" else status; notes.append(f"bare_months is {b.iloc[0]} in every year")
        bt = d.get("backtest")
        if not (bt and isnum(bt.get("n_seasons")) and len(bt.get("rows") or []) == 5):
            status = "FAIL"; notes.append("backtest missing or not 5 rows")
        else:
            notes.append(f"backtest n_seasons={bt['n_seasons']}, rows=5")
    if sf:
        sl = d.get("slope")
        if not (sl and isnum(sl.get("slope_pct")) and isnum(sl.get("elevation_m"))):
            status = "FAIL"; notes.append("slope/elevation missing")
        else:
            notes.append(f"slope {sl['slope_pct']} %, elevation {sl['elevation_m']} m")
    rep("C9", status, "; ".join(notes))

# C10 --------------------------------------------------------------------------
NUMRE = re.compile(r"(?<![\w.])\d+(?:\.\d+)?")
try:
    facts = open("facts.md", encoding="utf-8").read()
    src = "".join(open(f, encoding="utf-8").read() for f in ("ardi_summary.md", "ardi_data.json", "power_meta.json") if os.path.exists(f))
    tpl_path = next(iter(glob.glob("../drafts_from_claude/facts_TEMPLATE.md")), None)
    tpl = set(NUMRE.findall(open(tpl_path, encoding="utf-8").read())) if tpl_path else set()
    # URLs are not data values
    body = re.sub(r"https?://\S+", "", facts)
    nums = sorted(set(NUMRE.findall(body)), key=lambda x: float(x))
    def in_src(n): return re.search(r"(?<![\d.])" + re.escape(n) + r"(?!\d)", src) is not None
    notfound = [n for n in nums if not in_src(n) and n not in tpl]
    tplonly = [n for n in nums if not in_src(n) and n in tpl]
    ph = "[" in facts
    status = "FAIL" if ph or notfound else "PASS"
    rep("C10", status, f"'[' left: {ph}; numbers not found in summary/json/meta: {notfound or 'none'}; "
        f"template constants (not data, exempt): {tplonly or 'none'}")
except FileNotFoundError:
    rep("C10", "FAIL", "facts.md not found")

# C11 --------------------------------------------------------------------------
needle = "ey" + "J"                      # split so this file does not match itself
hits = []
for root, dirs, files in os.walk("."):
    dirs[:] = [x for x in dirs if x not in ("venv", "__pycache__", ".git")]
    for fn in files:
        path = os.path.join(root, fn)
        try:
            with open(path, "rb") as fh:
                if needle.encode() in fh.read(): hits.append(path)
        except OSError:
            pass
rep("C11", "FAIL" if hits else "PASS", f"files containing the token prefix: {hits or 'none'}")

print()
print("SUMMARY:", ", ".join(f"{c}={s}" for c, s, _ in results))
sys.exit(1 if any(s == "FAIL" for _, s, _ in results) else 0)
