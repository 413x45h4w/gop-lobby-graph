# Legislative layer (built 2026-11-22T20:30:12-05:00)

Sources (all public, no keys):
- GovInfo BILLSTATUS bulk XML, 118th + 119th Congress, all 8 bill/resolution types (https://www.govinfo.gov/bulkdata/BILLSTATUS/<congress>/<type>/BILLSTATUS-<congress>-<type>.zip, fetched 2026-11-22 ET; govinfo last-modified 2026-11-22 00:18 for 119 hr).
- unitedstates/congress-legislators `committee-membership-current.yaml`, `committees-current.yaml`, `legislators-current.json` (+ repo raw/legislators-historical.json for members who left after 2021).
- House Committee Repository event pages, docs.house.gov/Committee/Calendar/ByEvent.aspx?EventID=115150..119700 (Dec 2022 - Nov 2026): hearing/markup title, committee, date, witness name + title/organization (`raw/house_events.jsonl`; 711 ids had no event).
- GovInfo CHRG (published hearing transcripts) MODS metadata for every 118th/119th package in the public CHRG sitemaps 2023-2026 (`raw/chrg_mods.jsonl`): witnesses, committees, member roster printed in the record. House + Senate + Joint. Publication lags hearings by months, so recent Senate hearings are thin.

Files
- `bills.csv` one row per bill/resolution: sponsor bioguide, cosponsor counts, policy area, committee referrals, latest action, laws, top subjects.
- `bill_cosponsors.csv` every cosponsorship (incl. withdrawn, flagged) with date and original-cosponsor flag.
- `bill_committee_referrals.csv` bill -> committee/subcommittee with activities (Referred to, Markup by, Reported by...).
- `member_cosponsor_edges.csv` directed sponsor -> cosponsor edges (active cosponsorships only), n_bills, n_original, cross_party. Confidence high.
- `member_committee_edges.csv` member -> committee/subcommittee (current rosters; rank, title, majority/minority). Confidence high. Only current (119th) rosters are in this source; 118th rosters are not included.
- `committees.csv` committee code dictionary.
- `hearings.csv` hearing_id = `house:<EventID>` or `chrg:<package>`; the same House hearing can appear from both sources (edge aggregation de-duplicates witness appearances by date+committee+name).
- `hearing_witnesses.csv` every witness row with parsed org text, LD-2 org match, government-witness flag, lobbyist person match.
- `edges_witness_org_to_committee.csv` LD-2 client/registrant org -> committee: de-duplicated witness appearances, hearing days, date range. Confidence medium (org name match).
- `edges_lobbyist_witness_to_committee.csv` registered lobbyist who testified -> committee/hearing (high when name+org corroborated, low when name-only-unique).
- `hearing_members_listed.csv` members printed in CHRG hearing records (role COMMMEMBER etc.). This is the committee roster printed in the transcript, not proof of attendance.
- `dclib.py` shared matching helpers; `build_*.py`, `scrape_*.py` reproduce everything (scrapers resume).

Match rates and stats
```
{
 "hearings": 7217,
 "witness_rows": 22423,
 "org_committee_edges": 3428,
 "lobbyist_witness_rows": 1153,
 "hearing_member_rows": 98529,
 "witness": 22423,
 "org_match": 4937,
 "no_person_match": 21092,
 "name_only_ambiguous": 124,
 "name_only_unique": 679,
 "name+org_in_lda": 528,
 "built_at": "2026-11-22T20:23:34-05:00"
}
```
Witness org matching uses exact normalized names of whole comma-separated segments (1-3 segments), single-token keys must equal the full LD-2 name
(prevents e.g. "Enterprise" -> Enterprise Holdings). Known residual error: a witness's employer that shares a normalized name with an unrelated LD-2 client.

Match keys used across all four folders
- `bioguide`: Congress bioguide id (same ids as money_all/member_totals_all.csv and x_all/member_handles_all_party.csv).
- `lda_org_key`: normalized organization name (dclib.norm_org: upper-case, punctuation/legal suffixes INC/LLC/CORP/CO/GROUP/HOLDINGS/THE... removed)
  that equals a client or registrant name in the LD-2 universe in lda/ld2_universe (2022Q4-2026Q3, 315,129 filings). `lda_org_kinds`, `lda_client_ids`,
  `lda_registrant_ids` give the Senate LDA ids, so these rows join to LD-2 work in full/ld2/.
- `lobbyist_person_id`: person_id from money_all/people_all.csv (merged LDA lobbyist ids). Person matches are only emitted as
  `name+org_in_lda` (first+last name equals a lobbyist AND that lobbyist appears on an LD-2 filing for the matched org: confidence high) or
  `name_only_unique` (first+last equals exactly one lobbyist, no org corroboration: confidence low). Ambiguous names are never linked.
- Bill ids: `<type><number>-<congress>` lower-case, e.g. `hr1234-119`, `s50-118`, `hres12-119`.
- Committee codes: congress-legislators thomas ids, e.g. `HSWM` (House Ways and Means), `HSWM03` (subcommittee), `SSFI` (Senate Finance).
- Never fabricated: every row traces to a public source URL/file named below. Unmatched rows are kept with blank match columns.
- Append-only: rebuilding writes a `.prev_<YYYYMMDD_HHMM>` copy of any CSV it overwrites; raw/*.jsonl scrapes are append/resume files.

Row counts
| file | rows |
|---|---|
| `bill_committee_referrals.csv` | 56,626 |
| `bill_cosponsors.csv` | 394,117 |
| `bills.csv` | 39,512 |
| `committees.csv` | 230 |
| `edges_lobbyist_witness_to_committee.csv` | 1,153 |
| `edges_witness_org_to_committee.csv` | 3,428 |
| `hearing_members_listed.csv` | 98,529 |
| `hearing_witnesses.csv` | 22,423 |
| `hearings.csv` | 7,235 |
| `member_committee_edges.csv` | 3,895 |
| `member_cosponsor_edges.csv` | 115,313 |
| `raw/chrg_mods.jsonl` | 3,377 |
| `raw/house_events.jsonl` | 4,551 |

## Build log (append-only)
- 2026-11-22T20:30:02-05:00: rebuilt; counts above.
- 2026-11-22T20:30:12-05:00: rebuilt; counts above.
