# State-level and events layer (built 2026-11-22T20:30:12-05:00)

Built
- `member_caucus_edges.csv` caucus memberships: links inside the members sections of English Wikipedia caucus articles (revision ids in `source_ref`),
  resolved title -> Wikidata -> bioguide; plus Wikidata P463 statements whose label names a caucus/coalition. Confidence medium (crowd-sourced, can include
  members who left). Coverage is uneven: New Democrat Coalition resolves only a few members because the article lists members through templates;
  Republican Governance Group page includes historical Wednesday Group members. Page log: `raw/caucus_pages_log.json`.
- `house_foreign_travel_legs.csv` House official foreign travel (CODEL/STAFFDEL) legs parsed from the Clerk's text copies of the Congressional Record
  "Expenditure reports concerning official foreign travel" (2023-2026 releases, 71 files): traveler, member bioguide, dates, country, leg total USD.
- `edges_member_codel_cotravel.csv` member <-> member pairs listed in the same report with the same country and arrival/departure dates. Confidence high.

Gaps (recorded honestly)
- FollowTheMoney (state campaign finance): API requires a registered key ("Invalid API Key" without one); site says data current through 2024 and is being merged into OpenSecrets.
- OpenSecrets bulk data: behind a sign-in / bot check (HTTP 403 challenge); the OpenSecrets API has been discontinued. Not used.
- Political Party Time fundraiser archive: politicalpartytime.org returns HTTP 500 (offline).
- Senate foreign travel reports (Congressional Record, Senate section) not parsed yet.
- State lobbying registries: no free national bulk source; not built.

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
| `edges_member_codel_cotravel.csv` | 2,952 |
| `house_foreign_travel_legs.csv` | 6,831 |
| `member_caucus_edges.csv` | 1,402 |

## Build log (append-only)
- 2026-11-22T20:30:02-05:00: rebuilt; counts above.
- 2026-11-22T20:30:12-05:00: rebuilt; counts above.
