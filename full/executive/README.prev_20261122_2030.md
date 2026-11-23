# Executive-branch layer (built 2026-11-22T20:30:02-05:00)

Sources
- OIRA EO 12866 meetings, reginfo.gov public calendar (completed meetings 2023-01 .. 2026-11; detail pages with requestor + attendee list + org): `raw/oira_meetings.jsonl`.
  No published meetings appear for Oct 2025 (the calendar returns none for that month).
- White House visitor records (WAVES): the current administration does not publish them. A White House official said in Feb 2025 they would not be released
  during the second Trump term (reported by the Washington Examiner; logs are Presidential Records until 5 years after the term). Used instead: the Biden White House
  archive (bidenwhitehouse.archives.gov/disclosures/visitor-logs), files 2023.01 .. 2024.08 (the last release), streamed; only rows whose visitor first+last name equals
  an LDA lobbyist name were kept (`raw/wh_visitor_lobbyist_name_matches.jsonl`; per-file totals in `raw/wh_file_stats.jsonl`).
- regulations.gov comments: NOT built. The v4 API needs an api.data.gov key; DEMO_KEY is limited to 10 requests/hour on this IP and the comment list endpoint does not
  return the submitter organization (one call per comment needed). A free api.data.gov key (requires sign-up) or a targeted pull from the public Mirrulations S3 mirror
  (s3://mirrulations, per-comment JSON) would close this gap.
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
 "oira_meetings": 1357,
 "oira_attendees": 18284,
 "oira_attendee_gov": 11304,
 "oira_attendee_org_match": 3161,
 "oira_attendee_lobbyist_none": 17133,
 "oira_attendee_lobbyist_name_only_unique": 519,
 "oira_attendee_lobbyist_name+org_in_lda": 632,
 "wh_name_match_rows": 37381,
 "wh_ambiguous_name_excluded": 4398,
 "wh_tour_excluded": 15430,
 "wh_multi_middle_initial_excluded": 10697,
 "wh_kept": 6856,
 "oira_meetings_rows": 1357,
 "oira_attendee_rows": 18284,
 "org_agency_edges": 1160,
 "lobbyist_oira_rows": 1151,
 "wh_rows": 6856,
 "wh_edges": 5458,
 "built_at": "2026-11-22T20:28:47-05:00"
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
| `edges_lobbyist_to_agency_oira.csv` | 1,151 |
| `edges_lobbyist_to_wh_visitee.csv` | 5,458 |
| `edges_org_to_agency_oira.csv` | 1,160 |
| `oira_attendees.csv` | 18,284 |
| `oira_meetings.csv` | 1,357 |
| `wh_visits_lobbyist_name_matches.csv` | 6,856 |
| `raw/oira_meetings.jsonl` | 1,499 |
| `raw/wh_file_stats.jsonl` | 20 |
| `raw/wh_visitor_lobbyist_name_matches.jsonl` | 37,381 |

## Build log (append-only)
- 2026-11-22T20:30:02-05:00: rebuilt; counts above.
