/* Ardi scoring engine - reference implementation (contract v1).
   Reads ardi_data.json (Group C: NASA indicators) + crops.json (Group C: crop knowledge).
   Pure functions, no network. Works in the browser (window.ArdiScoring) and in Node (require).
   Rules (from the council):
   - Hard filter: no two crops of the same family in consecutive seasons, checked CYCLICALLY
     (the cycle repeats forever). The current rotation (A) is always shown, even if it breaks the rule.
   - 4 scores, each 0-1, or null = "not scored" when an input is missing (never a made-up number):
       water      share of past seasons with rain >= the crop's minimum, averaged over the plan
       stageRisk  share of past seasons WITHOUT a hit in the crop's sensitive stage
                  (heat: THRESHOLDS.heatDays or more days >32 C in Mar-May;
                   dry: THRESHOLDS.drySpells or more dry spells of >=10 days in Jan-Mar).
                  The two cut-offs are OUR CHOICE, not published values - change them only in THRESHOLDS below
                  and tell the team. The app prints them on screen from this object.
       soil       0.6 x share of legume seasons + 0.4 x (1 - typical bare months / 12)  [rule-based indicator]
       income     yield x price x that crop's water score, scaled to the best rotation shown [only if all inputs exist]
   - Dry line shown separately: does each crop's minimum rain fit inside the 5th-driest season? */
(function (root) {
  const DIMS = ["water", "stageRisk", "soil", "income"];
  const mean = a => a.length ? a.reduce((s, x) => s + x, 0) / a.length : null;
  const isNum = x => typeof x === "number" && !isNaN(x);
  // Stage-risk cut-offs (our choice; see data/stage_risk_and_benefits.md). Old rule was 1 heat day / any 10-day dry run.
  const THRESHOLDS = { heatDays: 5, drySpells: 3 };

  function expand(cycle, n) { const out = []; for (let i = 0; i < n; i++) out.push(cycle[i % cycle.length]); return out; }

  function familyBreaks(cycle, crops) {
    const fam = id => crops[id].family, br = [];
    for (let i = 0; i < cycle.length; i++) {
      const a = cycle[i], b = cycle[(i + 1) % cycle.length];
      if (fam(a) === fam(b)) br.push(`${crops[a].name_en} then ${crops[b].name_en} (both ${fam(a)})`);
    }
    return [...new Set(br)];
  }

  function cropWater(c, seasons) {
    if (!isNum(c.min_season_rain_mm)) return null;
    const s = seasons.filter(x => isNum(x.rain_mm));
    return s.length ? s.filter(x => x.rain_mm >= c.min_season_rain_mm).length / s.length : null;
  }

  function cropStage(c, seasons) {
    const r = c.stage_risk || {};
    const s = seasons.filter(x => (!r.heat_mam || isNum(x.heat_days_mam)) && (!r.dry_jfm || isNum(x.dry_spells_10d_jfm)));
    if (!s.length) return null;
    const hit = x => (r.heat_mam && x.heat_days_mam >= THRESHOLDS.heatDays) || (r.dry_jfm && x.dry_spells_10d_jfm >= THRESHOLDS.drySpells);
    return 1 - s.filter(hit).length / s.length;
  }

  function scoreRotation(rot, data, cropsDoc, horizon) {
    const crops = Object.fromEntries(cropsDoc.crops.map(c => [c.id, c]));
    const plan = expand(rot.cycle, horizon), list = plan.map(id => crops[id]);
    const seasons = data.seasons || [];
    const w = list.map(c => cropWater(c, seasons)), st = list.map(c => cropStage(c, seasons));
    const water = w.every(isNum) ? mean(w) : null;
    const stageRisk = st.every(isNum) ? mean(st) : null;
    const bare = list.map(c => c.bare_months_typical);
    const soil = bare.every(isNum) ? 0.6 * list.filter(c => c.legume).length / list.length + 0.4 * (1 - mean(bare) / 12) : null;
    const incomeRaw = list.every((c, i) => isNum(c.yield_t_ha) && isNum(c.price_ils_t) && isNum(w[i]))
      ? mean(list.map((c, i) => c.yield_t_ha * c.price_ils_t * w[i])) : null;
    const dl = data.dry_line;
    const dry = dl && list.every(c => isNum(c.min_season_rain_mm))
      ? { season: dl.season, rain_mm: dl.rain_mm, rank: dl.rank, n_seasons: dl.n_seasons,
          failing: [...new Set(list.filter(c => c.min_season_rain_mm > dl.rain_mm).map(c => c.name_en))] }
      : null;
    if (dry) dry.pass = dry.failing.length === 0;
    const breaks = familyBreaks(rot.cycle, crops);
    const statuses = [...new Set(list.map(c => c.status).concat(rot.status || []))];
    return { id: rot.id, rotation: rot, plan, crops: plan.map(id => crops[id]),
             scores: { water, stageRisk, soil, income: null }, incomeRaw, dry,
             filter: { pass: breaks.length === 0, breaks },
             illustrative: statuses.some(s => s !== "sourced" && s !== "local"),
             placeholderData: !!data.placeholder };
  }

  function rank(data, cropsDoc, weights) {
    const horizon = cropsDoc.horizon_seasons || 3;
    weights = Object.assign({ water: 1, stageRisk: 1, soil: 1, income: 1 }, weights || {});
    let out = cropsDoc.rotations.map(r => scoreRotation(r, data, cropsDoc, horizon))
      .filter(r => r.rotation.is_current || r.filter.pass);            // hard filter (current always shown)
    const maxInc = Math.max(...out.map(r => r.incomeRaw).filter(isNum));
    out.forEach(r => { r.scores.income = isNum(r.incomeRaw) && maxInc > 0 ? r.incomeRaw / maxInc : null; });
    out.forEach(r => {
      const used = DIMS.filter(d => isNum(r.scores[d]) && weights[d] > 0);
      const wsum = used.reduce((s, d) => s + weights[d], 0);
      r.total = used.length ? used.reduce((s, d) => s + weights[d] * r.scores[d], 0) / wsum : null;
      r.notScored = DIMS.filter(d => !isNum(r.scores[d]));
    });
    // current rotation first, then alternatives by total (unscored last)
    return out.sort((a, b) => (b.rotation.is_current - a.rotation.is_current) ||
                              ((isNum(b.total) ? b.total : -1) - (isNum(a.total) ? a.total : -1)));
  }

  const api = { rank, scoreRotation, expand, familyBreaks, DIMS, THRESHOLDS };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.ArdiScoring = api;
})(typeof window !== "undefined" ? window : globalThis);
