# Group C · crops.json v1 notes (for Rana) — written Sat 14 Nov, ~01:00

crops.json in this folder is a DRAFT v1. All four crops are marked "illustrative". Research was stopped part-way,
so some values are still null. Nothing was guessed: a value is either from the source listed or it is null.

## 1. What is filled and where it comes from

| Crop | min_season_rain_mm | yield_t_ha | bare_months_typical | price_ils_t |
|---|---|---|---|---|
| Wheat (durum) | 400 | 1.6 | 6 | 1766 |
| Barley | 200 | 1.4 | 6 | 2344 |
| Lentil | 250 | 1.16 | 6 | 4300 (assumption) |
| Bitter vetch | 300 | 1.29 | 6 | 2300 (assumption) |

(Table updated Sat 14 Nov ~07:40 to match crops.json. Prices: see section 5. The lentil and vetch yields were
filled after this note was first written; check crops.json `sources` for where they came from; the vetch yield has no yield source listed there, so confirm it.)

**min_season_rain_mm** = FAO ECOCROP "Rainfall (annual), absolute minimum".
- Durum wheat: absolute 400–800 mm, optimal 500–700. https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=10582
- Barley: absolute 200–2000, optimal 500–1000. https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=1232
- Lentil: absolute 250–2500, optimal 600–1000. https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=7209
- Bitter vetch: tolerates 300–1200, prefers 500–700. SECOND-HAND: this page quotes ECOCROP; I did not find the
  ECOCROP sheet itself. https://temperate.theferns.info/plant/Vicia+ervilia
- Why "illustrative": ECOCROP gives the ANNUAL rainfall range where the species can grow at all. It is not a
  tested "enough rain for a harvest in Jenin" threshold. Same source and same definition for all four crops, so
  the comparison between rotations is fair, but the absolute numbers are rough.
- Watch wheat = 400 mm. If the IMERG seasons at the point are often below 400 mm, wheat's water score will be low
  and it will fail the dry line. One paper describes rainfed wheat in Syria at 300–500 mm annual rainfall
  (https://www.cambridge.org/core/journals/renewable-agriculture-and-food-systems — search "Wheat farming in Syria:
  an approach to economic transformation and sustainability"; I saw only the abstract). If the team prefers a
  lower wheat threshold it needs its own source and must be said on screen.

**yield_t_ha**
- Wheat 1.6 and barley 1.4 t/ha: UNCTAD 2015, "The Besieged Palestinian Agricultural Sector", Table 3 (p. 4),
  rain-fed, whole Occupied Palestinian Territory, built from FAO and PCBS statistics of about 2010–2012.
  https://unctad.org/system/files/official-document/gdsapp2015d1_en.pdf
  National, old, not Jenin-specific. Replace if PCBS/MoA gives a Jenin figure.
- Lentil, bitter vetch: null. No Palestinian source found. (A Moroccan trial reports about 1 t/ha of bitter-vetch
  GRAIN — not hay, not local; not used.)

**bare_months_typical = 6 for all four** — our own estimate, not a sourced number.
- Winter planting of wheat and barley in the West Bank is Nov–Dec (FAO DIEM brief, Oct 2025):
  https://reliefweb.int/report/occupied-palestinian-territory/west-bank-diem-data-emergencies-brief-food-security-and-livelihoods-agricultural-households-october-2025
- Wheat harvest photographed 13 May 2013 at Tammun (FAO):
  https://digital-media.fao.org/archive/WEST-BANK--Tammun--2013--Harvesting-Wheat--2A6XC587F9AU.html
- Sown about December, cut about late May/June gives roughly 6 months with no living crop. I found no
  crop-by-crop calendar, so all four crops have the same value and the soil score differs only by the legume share.
  The MODIS bare-months number in ardi_data.json is the measured one; this is only the fallback.

**price_ils_t = null for all.** No farm-gate price found. WFP's market dashboards give RETAIL lentil prices
(about 7.2 NIS/kg in the West Bank, mid-2022) — that is a shop price for mostly imported lentils, not what a
farmer receives, so it is not used. Effect: the Income score shows "not scored" for all three rotations.
Best fix: ask the farmer / extension officer for last season's selling prices (status "local").

**stage_risk true/false flags** came pre-filled in the template. I found no source for them and did not change
them. Confirm each with an agronomist or say on screen that they are assumptions.

## 1b. Update at ~04:10 (after the real NASA data came in)
Real data at the point (IMERG): 27-season mean 473 mm; 5th-driest season 2007/08 = 363 mm.
- WHEAT 400 mm decides the result: with 400, wheat fails the dry line (363 < 400); barley, lentil and
  bitter vetch pass. FAO's dryland-wheat chapter says Mediterranean durum wheat is typically grown in
  medium-rainfall areas of 250-450 mm average annual rain (https://www.fao.org/4/Y4011e/y4011e0s.htm).
  That is a zone where durum is grown, not a crop minimum. We KEEP 400 (ECOCROP absolute minimum) so all
  four crops use the same source and definition. Say on screen: "rain minimums: FAO ECOCROP, illustrative".
  If the team prefers the FAO zone figure, use the same kind of figure for all four crops, never mix.
- LENTIL 250 mm is now backed by a Palestinian field study too: lentil is not recommended below 250 mm
  (IUG Journal of Natural Studies 29(1), 2021; https://search.emarefa.net/en/detail/BIM-1380580-effects-of-climatic-gradient-on-growth-performance-yield-com).
- LENTIL yield 1.71 t/ha: FAOSTAT figure for Palestine, 2019 (17,141 hg/ha), read from an aggregator page
  (https://d3fqfiq2w1ez7u.cloudfront.net/nmx/timeseries/palestine-lentils-yield). National average, may
  include irrigated land; verify on FAOSTAT if there is time.
- BITTER VETCH yield 1.29 t/ha (grain, dry matter): conservative end of 1,285-1,959 kg/ha across 25
  accessions over four seasons in dryland north-west Syria (ICARDA trial, Animal Feed Science and
  Technology 165, 2011; https://repo.mel.cgiar.org/items/594a548e-3d93-47fb-8b72-cb50a3f691dc).
  Trial plots, not farms; hay yield (2,738-3,435 kg DM/ha) is the other use if cut green.
- PRICES still null. Only a Jordanian government procurement price was found (420 JOD/t wheat, 370 JOD/t
  barley, 2024/25) - another country, another currency, subsidised: not used. Ask in the farmer call.

## 1c. stage_risk flags, researched (~04:45). Only true/false values changed; no keys added or removed.
heat_mam = a day >32 C in Mar-May hurts the crop (flowering / grain or pod filling).
dry_jfm  = a dry spell of 10+ days in Jan-Mar hurts the crop (seedling / vegetative growth).
| crop | heat_mam | dry_jfm | evidence |
|---|---|---|---|
| wheat | true | true | 32/22 C for 14 days at anthesis or grain filling cut grain yield 29% and 44% (BMC Plant Biol 2020, PMC7285450). dry_jfm: no specific source found; kept from template |
| barley | true | true | wheat and barley yields fall with heat above optimum (review, PMID 32667992); barley often damaged by days >30 C during flowering and grain development (Front Plant Sci 2022). dry_jfm: no specific source; kept from template |
| lentil | true | true (was false) | temperatures over 32 C at flowering and podding damage reproductive organs (Front Nutr 2022); lentil is highly sensitive to drought at seedling and flowering stages (Front Plant Sci 2024 review) -> Jan-Mar seedling stage counts |
| bitter vetch | true (was false) | false (was true) | terminal heat stress is studied as a yield constraint in bitter vetch (Iran field trial, 2026); being earlier than other vetches does not show it escapes Mar-May heat. Resistant to drought even in the early growing period (ECOCROP, via Useful Temperate Plants) and relatively drought-tolerant (Plants 2025) |
Effect with the real data and current scoring.js rule (any single event = hit): stage risk A 0.00, B 0.00,
C 0.02. Totals: A 0.33, B 0.42, C 0.47. Stage risk still does not separate rotations; the threshold is
Sameer's call (see the threshold table in chat) and must be stated on screen.
Still "illustrative": the 32 C / 10-day thresholds and the Jan-Mar / Mar-May windows come from the plan,
and these are general crop studies, not Jenin field data. Ask the farmer.

## 1d. Item 13 checked (~04:55)
- LENTIL YIELD changed 1.71 -> 1.16 t/ha. FAOSTAT via Helgi Library: 2022 production 784 t on 678 ha
  = 1.16 t/ha; 2021 was a near-failure (42 t). Method check: 2019 gives 1,361 t / 794 ha = 1.71, matching the
  FAOSTAT yield page (17,141 hg/ha). Yield swings ~1.0-1.7 t/ha; 1.16 is the latest year and the conservative end.
- WHEAT/BARLEY dry_jfm = true now sourced. Wheat (Israel, Mediterranean): under low rain, drought stress came
  during stem elongation and cut yield through fewer ears (Blum & Pnuel 1990, https://publish.csiro.au/cp/AR9900799).
  Barley (Jordan/ICARDA): pre-anthesis drought (tillering, stem elongation) reduced grain yield and grain number
  in all genotypes (Al-Ajlouni et al. 2016, https://repo.mel.cgiar.org/items/0463bba4-d4d8-48fd-9e18-04a3d5461112/full).
- PCBS 95.8%: still NOT confirmed directly (the PDF blocks automated reading). Two official PCBS tables:
  (a) 2010/11: Jenin field crops 98.8% rainfed, 1.2% irrigated
      (https://pcbs.gov.ps/Portals/_Rainbow/Documents/Agri.2010-2011,18E.htm).
  (b) Census 2021: Jenin TEMPORARY crops (field crops + vegetables) 74.5 km2 rainfed vs 31.4 km2 irrigated
      (https://pcbs.gov.ps/Portals/_Rainbow/Documents/LUS2E.html).
  The claim (73,973 of 77,183 dunums field crops rainfed) fits inside (b): 74.0 km2 rainfed <= 74.5, 3.2 km2
  irrigated <= 31.4. Consistent, not proven. Safe wording now: "PCBS 2010/11: 98.8% of Jenin's field-crop area
  was rainfed." Use 95.8% only after Rana sees it in book2649.pdf.

## 2. PCBS check — NOT verified
"73,973 of 77,183 dunums of field crops in Jenin rainfed (95.8%)". The PCBS site blocks automated reading of
https://www.pcbs.gov.ps/Downloads/book2649.pdf and web search did not surface the two numbers, so I could not
confirm or correct it. Rana: open the PDF, find the table "area of field crops by governorate and irrigation
type", check both numbers and note the table number and page. The arithmetic is right (73,973 / 77,183 = 95.8%).
Only as a plausibility check, not a substitute: PCBS's 2010/2011 national figure is 230,815 rainfed vs 14,599
irrigated dunums of field crops (94.1% rainfed). https://www.pcbs.gov.ps/MIndicators.aspx?pageId=115

## 3. Red flag for rotations B and C — ask in the call
A 2021 agro-biodiversity report on Jenin Governorate (RWDS) appears to say that lentils are rarely grown at
economic scale there and that barley is no longer grown; it also says wheat is 99% rainfed. I saw only the
search excerpt, not the full report, so read it before quoting:
http://rwds.ps/imgs/post/2021/8/19/UGPVZFPHIHTSRGRDTTKPWPRHYGSZECJVDZFBCHWA/65960997554.pdf
An ESCWA summary on Marj Ibn Amer lists barley among Jenin's known crops, so the picture is mixed:
https://unescwa.org/sites/default/files/inline-files/national-assessment-report-palestine-summary-english_0.pdf
If farmers there really do not grow lentil or barley, the pitch should say B and C are "alternatives to test",
and the call should ask why they stopped (seed, price, labour, broomrape?).

## 4. For a local agronomist to check (from general agronomy knowledge, no source attached)
- Sowing and harvest dates for each of the four crops in the Jenin plain.
- Broomrape (Orobanche) in lentil and bitter vetch fields.
- Bitter vetch: nitrogen left in the soil is much smaller when it is cut for hay than when ploughed in.
- Bitter vetch grain is normally fed to ruminants (sheep, goats), not poultry or people, unless treated.
- Seed availability for lentil and bitter vetch; whether the farmer has livestock or a buyer for vetch.
- Wheat after barley is still cereal after cereal (the app's filter already blocks it).

## 5. Farmer-card sentences
Already inside crops.json as card_ar / card_en on each rotation (the new contract field). Rana, please read
the Arabic aloud and fix anything that does not sound like Jenin speech. The reasons used are only these:
lentil and barley have a lower rain minimum than wheat (ECOCROP figures above); legumes feed the soil.

## 6. Call script (about 5 minutes; no names written down)
Opening — consent first:
"مرحبا، أنا رنا من جامعة بيرزيت. إحنا فريق طلاب بنشتغل على مشروع عن الدورة الزراعية والمطر. ممكن أسألك خمس أسئلة
قصيرة؟ ما رح ننشر اسمك ولا مكان أرضك بالضبط. موافق نستخدم إجاباتك بالمشروع؟"
(Hello, I'm Rana from Birzeit University. We're a student team working on crop rotation and rain. May I ask five
short questions? We won't publish your name or your exact location. Do you agree that we use your answers?)
If the answer is no: thank them and stop.

1. "شو زرعت بالأرض البعلية آخر ثلاث مواسم؟ وبأي ترتيب؟"
   (What did you plant on the rainfed land in the last three seasons, in what order?)
2. "بتتذكر موسم كان سيّئ كثير من قلّة المطر؟ أي سنة؟ وشو صار بالمحصول؟"
   (Do you remember a very bad season because of low rain? Which year? What happened to the crop?)
3. "إمتى بتزرع العدس عادةً، وإمتى بتحصده؟ وإذا ما بتزرعه، ليش؟"
   (When do you usually sow and harvest lentil? If you don't grow it, why not?)
4. "عندك مواشي؟ وبتزرع كرسنة أو شعير علف إلهم؟"
   (Do you keep livestock? Do you grow bitter vetch or barley to feed them?)
5. "بكم بعت القمح (والعدس أو الشعير إذا في) آخر موسم، بالشيكل للكيلو أو للطن؟"
   (What price did you get for wheat — and lentil or barley if any — last season, in shekels per kg or ton?)
Closing: "شكراً كثير. مرة ثانية: ما رح نذكر اسمك."
Write down: date and time of the call, governorate/village level only, and the answers word for word.
Question 5 replaces a separate consent question because consent is asked at the start; it is the only way we
currently have to fill price_ils_t.

## 5. Prices added Sat 14 Nov ~07:15 (price_ils_t was null; Yara asked for it to be filled)
Unit: NIS per tonne, farm-gate. All four crops stay status "illustrative" (yield etc. are still illustrative).
- WHEAT 1766 = PCBS Average Producer Prices 2021, "Anbar Wheat" 88.30 NIS per 50 kg sack x 20.
  (American wheat was 81.46.) https://pcbs.gov.ps/Portals/_Rainbow/Documents/Other-2021-E-16.htm
- BARLEY 2344 = same PCBS table, 117.18 NIS per 50 kg x 20, rounded.
  Note: 2021 prices, not this season. Barley above wheat is what PCBS reports for 2021.
- LENTIL 4300 = ASSUMPTION, no farm-gate source found. PCBS has no lentil row. Basis: WFP retail lentil about
  7.2 NIS/kg (West Bank, Jun 2022) x 0.6 as a guess at the farmer's share. Replace with Rana's farmer-call price.
  https://www.un.org/unispal/wp-content/uploads/2022/08/WFPMOMKTDBJUNE22_300622.pdf
- BITTER VETCH 2300 = ASSUMPTION, no price found anywhere (not in PCBS 2017 or 2021). Set about equal to barley as
  a feed grain. Replace with a real price.
The screen must say prices are assumptions / 2021 averages. With these four numbers the Income preset now differs
from Balanced (income per ha: wheat ~2826, barley ~3282, lentil ~4988, vetch ~2967 NIS).
