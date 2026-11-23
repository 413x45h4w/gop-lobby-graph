# Executive-branch layer (built 2026-11-22T21:14:37-05:00)

Sources
- OIRA EO 12866 meetings, reginfo.gov public calendar (completed meetings 2023-01 .. 2026-11; detail pages with requestor + attendee list + org): `raw/oira_meetings.jsonl`.
  No published meetings appear for Oct 2025 (the calendar returns none for that month).
- White House visitor records (WAVES): the current administration does not publish them. A White House official said in Feb 2025 they would not be released
  during the second Trump term (Washington Examiner report, as cited by Vox Luci on 2026-11-15; logs are Presidential Records until 5 years after the term). Used instead: the Biden White House
  archive (bidenwhitehouse.archives.gov/disclosures/visitor-logs), files 2023.01 .. 2024.08 (the last release), streamed; only rows whose visitor first+last name equals
  an LDA lobbyist name were kept (`raw/wh_visitor_lobbyist_name_matches.jsonl`; per-file totals in `raw/wh_file_stats.jsonl`).
- regulations.gov comments: the v4 API needs an api.data.gov key (DEMO_KEY = 10 requests/hour here, and list results lack the submitter organization), so the
  official API was not used. Instead a bounded pull from the public Mirrulations S3 mirror of regulations.gov (s3://mirrulations, AWS Open Data, Moravian University):
  rulemaking dockets opened 2025-2026 whose RIN also had an OIRA EO 12866 meeting in 2025-2026, at most 800 comment JSONs per docket (see `docket_n_comments_in_mirror`
  for the true size). `raw/regs_dockets.jsonl`, `raw/regs_comments.jsonl`, `regs_comments_orgs.csv`, `edges_org_to_docket_comments.csv`. This is a sample, not full coverage.
- Agency calendars: no central structured source; not built.

Files
- `oira_meetings.csv` meeting, date, RIN, rule title, agency, stage, requestor org/name, requestor LD-2 org keys.
- `oira_attendees.csv` every attendee with org, government flag, LD-2 org keys (firm / client roles when written "X on behalf of Y"), lobbyist match.
- `edges_org_to_agency_oira.csv` LD-2 org -> agency (n meetings, RINs). Confidence high for the org name match (exact normalized; a short list of unambiguous trade-group acronyms EEI, API, NAM, ACC, AFPM, PhRMA, NRECA, APPA, INGAA, NMA, AGC, NAHB, NFIB, IPAA, AHIP, NRDC, EDF is expanded).
- `edges_lobbyist_to_agency_oira.csv` lobbyist -> agency/rule meetings.
- `wh_visits_lobbyist_name_matches.csv`, `edges_lobbyist_to_wh_visitee.csv` LOW confidence, name-only: visitor first+last equals exactly one LDA lobbyist,
  public tours excluded, names seen with more than one middle initial excluded, `large_event_gt50` flags receptions/events. Treat as leads, not confirmed ties.

Stats
```
{
 "oira_meetings": 3277,
 "oira_attendees": 41008,
 "oira_attendee_gov": 24645,
 "oira_attendee_org_match": 7381,
 "oira_attendee_lobbyist_none": 38243,
 "oira_attendee_lobbyist_name_only_unique": 1250,
 "oira_attendee_lobbyist_name+org_in_lda": 1515,
 "wh_name_match_rows": 37381,
 "wh_ambiguous_name_excluded": 4398,
 "wh_tour_excluded": 15430,
 "wh_multi_middle_initial_excluded": 10697,
 "wh_kept": 6856,
 "regs_comments": 56396,
 "regs_comments_with_org": 6183,
 "regs_comments_org_match": 2234,
 "regs_comment_org_rows": 6183,
 "org_docket_edges": 2037,
 "regs_dockets_scanned_2025_26": 20549,
 "regs_dockets_with_comments_fetched": 83,
 "oira_meetings_rows": 3277,
 "oira_attendee_rows": 41008,
 "org_agency_edges": 2274,
 "lobbyist_oira_rows": 2765,
 "wh_rows": 6856,
 "wh_edges": 5458,
 "built_at": "2026-11-22T21:13:48-05:00"
}
```

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
| `edges_lobbyist_to_agency_oira.csv` | 2,765 |
| `edges_lobbyist_to_wh_visitee.csv` | 5,458 |
| `edges_org_to_agency_oira.csv` | 2,274 |
| `edges_org_to_docket_comments.csv` | 2,037 |
| `oira_attendees.csv` | 41,008 |
| `oira_meetings.csv` | 3,277 |
| `regs_comments_orgs.csv` | 6,205 |
| `wh_visits_lobbyist_name_matches.csv` | 6,856 |
| `raw/oira_meetings.jsonl` | 3,277 |
| `raw/regs_comments.jsonl` | 56,396 |
| `raw/regs_dockets.jsonl` | 21,635 |
| `raw/wh_file_stats.jsonl` | 20 |
| `raw/wh_visitor_lobbyist_name_matches.jsonl` | 37,381 |

## Build log (append-only)
- 2026-11-22T20:30:02-05:00: rebuilt; counts above.
- 2026-11-22T20:30:12-05:00: rebuilt; counts above.
- 2026-11-22T20:35:36-05:00: rebuilt; counts above.
- 2026-11-22T21:13:40-05:00: rebuilt; counts above.
- 2026-11-22T21:13:50-05:00: rebuilt; counts above.
- 2026-11-22T21:14:38-05:00: rebuilt; counts above.
