# outside_money/: independent expenditures and super PAC money (FEC)

Built 2026-11-22 ET (America/New_York) by `scripts/*.py`. Data is append-only: later rebuilds keep prior outputs as `*.prev_<YYYYMMDD_HHMM>.*`.
All files are derived from public FEC bulk data. Nothing is inferred beyond the stated matching rules. Gaps are listed at the bottom.

## Sources
| source | file | as of |
|---|---|---|
| FEC independent expenditures (Schedule E + 24/48-hour reports), 2024 and 2026 cycles | `https://www.fec.gov/files/bulk-downloads/{2024,2026}/independent_expenditure_{y}.csv` (raw/, not committed) | downloaded 2026-11-22 20:09 ET |
| FEC individual contributions bulk (`indiv24.zip`, `indiv26.zip`, already in `money_all/raw/fec_bulk/`) | streamed; receipts of IE-only (type O), single-candidate IE (U), hybrid (V/W) committees and non-committee IE filers (type I / not in master), written to raw/superpac_receipts{24,26}.txt.gz (not committed) | FEC files dated 2026-11-15 |
| FEC committee master `cm24/cm26` | `money_all/raw/fec_bulk/` | 2026-11-18 |
| Lobbyist universe | `money_all/people_all.csv` (`person_id`, 21,408 people) | 2026-11-18 |
| LDA client spend | `boards/lda_clients_spend_2023_26.csv` (local LD-2 crawl, 2023-2026) | 2026-11-22 |

No FEC API calls were needed (key unused; never printed).

## Files
| file | rows | what |
|---|---|---|
| `edges_ie_spender_to_member.csv` | 3,541 | **spender→member support/oppose edges**, aggregated per (spender_id, bioguide, support/oppose, cycle): usd, n_expenditures, first/last date, spender_type, connected org. 780 spenders, 404 current members. |
| `ie_expenditures_dedup.csv` (gitignored; `.csv.gz` committed) | 104,907 | row-level deduplicated IEs (all candidates incl. presidential and non-members). `bioguide` is filled when `cand_id` is a current member's FEC id (congress-legislators). Has `fec_url`, `quality_flag`. |
| `edges_lobbyist_to_superpac.csv` | 4,253 | row-level lobbyist→super PAC/hybrid contributions 2023-26, matched to `people_all.person_id` |
| `edges_lobbyist_to_superpac_agg.csv` | 1,938 | the same aggregated per (person_id, committee, cycle), with the committee's IE party lean and the lobbyist's share of its itemized receipts |
| `superpac_lobbyist_ambiguous.csv` | 286 | same-name hits not attributed (several candidates / weak evidence) |
| `edges_client_org_to_superpac_rows.csv` / `_agg.csv` | 4,289 / 1,567 | **LDA clients (companies, unions, associations) that gave to super PACs as organizations**: FEC contributor name (entity ORG/CORP/COM/PAC) normalized == LDA client (or registrant) name normalized. $1.20B total. |
| `edges_client_employees_to_superpac.csv` | 31,438 | individuals whose self-reported employer == an LDA client name, aggregated per (client, committee, cycle). **Signal only: personal money, not the company's.** |
| `superpac_committees_receipts.csv` | 3,690 | itemized non-memo receipts per committee and cycle (conduits excluded) |
| `superpac_top_donors.csv` | 5,000 | top donor/committee/cycle pairs, summed over itemized rows of at least $1,000 |
| `outside_spenders_summary.csv` | 3,008 | one row per spender or committee: IE lean (R share of D/R support+oppose dollars; R ≥0.8, D ≤0.2, else mixed), IE $ for current members, itemized receipts |
| `ie_stats.json`, `superpac_match_stats.json`, `summary_stats.json` | | run statistics |

### Key schema / match keys
- Members: `bioguide` (same as `money_all/member_totals_all.csv`, `edges_fec_all.csv`).
- Lobbyists: `person_id` (= `money_all/people_all.csv`, which merges LDA lobbyist ids; `lobbyist_universe_scored.csv.lda_lobbyist_id` maps through `people_all.person_key`, which lists the merged LDA ids separated by `|`).
- Committees: `fec_committee_id` (same as `money_all/edges_lobbyist_to_pac_all.csv`).
- LDA clients: `client_key` = normalized name (`boards/scripts/orgnorm.py`), joins `boards/lda_clients_spend_2023_26.csv`.

## Rules
- **IE dedup:** key (spe_id, tran_id); keep the row from the highest `file_num`. 124,850 raw rows became 104,907.
- **IE quality:** 37 rows filed through the FEC web form (`tran_id` WFT…) with single amounts of at least $1M are flagged `excluded_implausible_webform` and left out of every aggregate. They total $81.4B of obvious junk (e.g. "$9,978,412,568 Political Contribution"). Smaller web-form rows are kept and flagged `webform_filer`.
- **IE totals:** $7.70B of non-excluded IEs across all candidates. Of that, **$1.99B targeted current members** ($0.90B in the 2024 cycle, $1.09B in 2026).
- **Super PAC donors, lobbyists:** the exact index and confidence rules of `money_all/fec_match_all.py`, executed from its source:
  - `high_employer_matches_registrant`: name plus employer matching the lobbyist's LDA registrant
  - `medium_lobbying_occupation`
  - `low_dc_area_professional`
  - Ties or contradictions go to the ambiguous file.
- **Conduits excluded:** ActBlue (C00401224) and WinRed (C00694323) are registered as hybrid PACs, but their receipts are earmarked pass-throughs to candidates. 19.76M rows were skipped. Memo rows (memo_cd X) and rows dated before 2023 were skipped too.
- **Hybrid PACs (V/W)** are included but labelled. Their receipts mix the contribution and non-contribution accounts.

## Match rates
- 28.1M super PAC/hybrid receipt rows (2023-26). 185,493 same-name hits against the lobbyist index.
- 4,253 attributed rows: 2,967 high, 345 medium, 941 low. They cover **1,282 lobbyists and $4.69M** ($3.53M at high confidence).
- 286 ambiguous rows. 180,954 rejected for lacking employer or occupation evidence.

## Notable
- Biggest IE totals against current members: Jon Husted (opposed $129.7M, supported $67.8M), Bernie Moreno, Dave McCormick, Tim Sheehy.
- Top spenders: WinSenate ($294M), HMP ($227M), Defend American Jobs ($121M), AFP Action ($82M), Protect Progress ($46M).
- Lobbying clients giving to super PACs as organizations include:
  - Coinbase, Ripple, Jump Crypto and a16z to Fairshake and Leading the Future
  - LCV to LCV Victory Fund
  - the Carpenters union
  - AIPAC to United Democracy Project
  - FanDuel to Win for America
  - NAR
- Largest lobbyist donors to super PACs: Heather Podesta (SMP, HMP), Emanuel Rouvelas (VoteVets), James Murphy (Commonwealth Unity Fund), Mike McKay (HMP).

## Gaps
- Contributions from other committees to super PACs (FEC `oth` / Schedule A from committees) are **not** included; only the individual/organization file was used. The `oth24/26` bulk files were not on the box.
- Client↔super PAC organization matching is exact on normalized names. Subsidiaries and DBA names are missed (e.g. "Coinbase Global" vs "Coinbase, Inc." only if normalization collapses them).
- Some super PACs' IE party lean is empty because their IEs are filed under a different committee id (e.g. SMP's spending goes through WinSenate).
- 24/48-hour notices and later Schedule E lines with different `tran_id`s can still double count. FEC data quality; not corrected beyond the tran_id dedup.

## Run log (append-only)
- 2026-11-22 20:09-20:33 ET: first build. Run 1 included ActBlue/WinRed and was discarded before any outputs were committed (its log is kept as `superpac_match.run1_with_conduits.log`). Run 3 used the apostrophe-fixed org normalizer.
