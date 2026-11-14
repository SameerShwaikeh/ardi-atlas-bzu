# Ardi data contract v1 (locked at 01:30 AM — change only with all three groups agreeing)

Two JSON files connect the groups. The app reads ONLY these two files.

| File | Made by | Read by | How |
|---|---|---|---|
| `ardi_data.json` | Group C (Mahmoud) — written by `3_indicators.py` | Group A app + scoring | NASA indicators for one point |
| `crops.json` | Group C (Rana) — filled by hand, with sources | Group A app + scoring | Crop traits + the 3 rotations |
| `ardi_data.placeholder.json` | ready now | Group A until real data lands | Same shape, `"placeholder": true`, SYNTHETIC numbers |

## ardi_data.json
```
{
 "contract_version": 1,
 "placeholder": false,                // true = synthetic; the app MUST show a red "test data" banner
 "generated": "2026-11-14T04:10",
 "point": {"name": "...", "lat": 32.xx, "lon": 35.xx},
 "datasets": [ {"id": "imerg|power|modis|srtm", "label": "full label with resolution + date range", "role": "..."} ],
 "seasons": [ {                       // one per complete Oct-May season, oldest first
    "season": "2010/11",
    "rain_mm": 452.8,                 // IMERG Oct-May total
    "rank_driest": 5,                 // 1 = driest of all IMERG seasons
    "days_ge20mm": 4,
    "dry_spells_10d_jfm": 0, "longest_dry_run_jfm": 7,
    "heat_days_mam": 0, "frost_days": 3,     // POWER (may be missing)
    "bare_months": 6,                 // MODIS, Oct-Sep year (may be missing)
    "ndvi_peak": 0.602                // MODIS Dec-May peak (may be missing)
 } ],
 "dry_line": {"season": "2010/11", "rain_mm": 452.8, "rank": 5, "n_seasons": 27, "pct_of_mean": 89, "mean_rain_mm": 507},
 "slope": {"slope_pct": 0.6, "elevation_m": 150, "note": "..."} | null,
 "backtest": {"n_seasons": 25, "driest_below_mean": 3, "driest_below_1sd": 2, "spearman_rain_vs_ndvi": 0.26,
              "rows": [ {"season": "...", "rain_mm": 0, "rank": 1, "ndvi_peak": 0.0, "anomaly_sd": 0.0} ]} | null
}
```
Any field may be missing or null. The app shows "not scored" / "no data" — never a default number.

## crops.json
- `crops[]`: id, name_en, name_ar, family (`cereal`|`legume`), legume, `min_season_rain_mm`, `stage_risk {heat_mam, dry_jfm}`,
  `bare_months_typical`, `yield_t_ha`, `price_ils_t`, `status` (`sourced`|`local`|`illustrative`|`todo`), `sources[]` (URLs).
- `rotations[]`: id A/B/C, labels EN/AR, `cycle` (repeats forever), `is_current`, `status`, `note`.
- Optional per rotation: `card_ar`, `card_en` — the farmer-card sentence (Rana). Missing = placeholder shown.
- `horizon_seasons`: 3 (the plan shows the cycle over 3 seasons).
- Current rotations: A = wheat every year · B = wheat ↔ lentil · C = barley ↔ bitter vetch (كرسنة).

## scoring.js
Reference engine (tested in Node): `ArdiScoring.rank(ardiData, crops, weights)` → rotations with
`scores {water, stageRisk, soil, income}` (0–1 or null), `total`, `dry {pass, failing, season, rain_mm, rank, n_seasons}`,
`filter {pass, breaks}`, `illustrative`, `placeholderData`, `notScored`. Run `node test_scoring.js` to see it work.
Thresholds live at the top of the file comment; change them there only and tell the team.
