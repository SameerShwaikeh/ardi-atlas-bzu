# Stage-risk threshold + card "Benefits" lines (drafted Sat 14 Nov ~07:20, for Sameer / Yara to approve)

## 1. Stage-risk threshold — recommendation
Counts below are from ardi_data.json, 27 seasons (1998/99-2024/25), Jenin plain point. Re-count after the 08:00 data.

| rule | seasons flagged (of 27) |
|---|---|
| heat: >=1 day above 32 C in Mar-May | 25 |
| heat: >=3 days | 18 |
| heat: >=5 days | 10 |
| heat: >=8 days | 2 |
| heat: >=14 days (the exposure in the lab study) | 0 |
| dry: >=1 spell of 10+ dry days in Jan-Mar | 23 |
| dry: >=2 spells | 17 |
| dry: >=3 spells | 10 |
| dry: >=4 spells | 1 |

"Any single event" flags almost every season (25 and 23 of 27), so it cannot tell rotations apart.
The study's 14 days flags none (max in the record is 8). So the cut-off has to be a choice in between.

RECOMMENDED: heat hit = 5+ days above 32 C in Mar-May; dry hit = 3+ dry spells of 10+ days in Jan-Mar.
Each flags 10 of 27 seasons (37%). Either one: 16 of 27. Both: 4 of 27.

HONEST LABEL: the 32 C figure and the 10-day dry spell come from crop studies (see rana_notes.md 1c).
The 5-day and 3-spell cut-offs are OUR CHOICE. No published threshold exists for Jenin; they were picked so the check
flags roughly 1 season in 3. Do not call them sourced.
Heat comes from NASA POWER (T2M_MAX, a ~55 x 59 km grid cell), so it is coarse for one farm.

ON-SCREEN LINE (EN): A season counts as a stage hit if it has 5+ days above 32 C in March-May, or 3+ dry spells of
10+ days in January-March. These cut-offs are our choice, not a published threshold.
ON-SCREEN LINE (AR): الموسم بنحسبه "ضربة" إذا فيه 5 أيام أو أكثر فوق 32 درجة بين آذار وأيار، أو 3 فترات جفاف أو أكثر
(كل وحدة 10 أيام أو أكثر) بين كانون الثاني وآذار. هاي الحدود اختيار منّا، مش رقم منشور.

scoring.js is not in the repo, so nothing was changed there. Change the two numbers where its threshold comment says to,
and tell the team (DATA_CONTRACT.md).

## 2. "Benefits" line per rotation (uses only numbers already in crops.json; rain minimums are ECOCROP)
A (current, wheat every year)
  EN: Familiar crop, no change needed, but no legume to feed the soil.
  AR: محصول مألوف وما بدّه تغيير، بس ما في بقوليات تغذّي التربة.
B (wheat <-> lentil)
  EN: Lentil needs less rain than wheat (250 vs 400 mm minimum) and feeds the soil.
  AR: العدس بيحتاج مطر أقل من القمح (250 مقابل 400 ملم كحد أدنى) وبغذّي التربة.
C (barley <-> bitter vetch)
  EN: Barley copes with low rain (200 vs 400 mm minimum for wheat); vetch feeds the soil and your animals.
  AR: الشعير بيتحمّل قلّة المطر (200 مقابل 400 ملم كحد أدنى للقمح)، والكرسنة بتغذّي التربة ومواشيك.
Rana: read the Arabic aloud and fix anything that does not sound like Jenin speech.
Caveat: RWDS 2021 may say lentil/barley are rarely grown in Jenin (rana_notes.md section 3). Keep "alternatives to test".
