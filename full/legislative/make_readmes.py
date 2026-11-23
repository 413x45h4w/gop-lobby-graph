# Writes README.md for legislative/, executive/, ethics/, state_events/ with live row counts. Keeps .prev_ copies (append-only rule).
import os,glob,csv,json,dclib
F=dclib.ROOT
def rc(fn):
  with open(fn) as f: return sum(1 for _ in f)-1
def table(d):
  out=['| file | rows |','|---|---|']
  for fn in sorted(glob.glob(os.path.join(F,d,'*.csv'))):
    if '.prev_' in fn: continue
    out.append(f'| `{os.path.basename(fn)}` | {rc(fn):,} |')
  for fn in sorted(glob.glob(os.path.join(F,d,'raw','*.jsonl'))):
    out.append(f'| `raw/{os.path.basename(fn)}` | {rc(fn)+1:,} |')
  return '\n'.join(out)
def stats(d,fn):
  p=os.path.join(F,d,fn)
  return '```\n'+json.dumps(json.load(open(p)),indent=1)+'\n```' if os.path.exists(p) else ''
COMMON="""Match keys used across all four folders
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
- Append-only: rebuilding writes a `.prev_<YYYYMMDD_HHMM>` copy of any CSV it overwrites; raw/*.jsonl scrapes are append/resume files."""
R={}
R['legislative']=f"""# Legislative layer (built {dclib.NOW()})

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
{stats('legislative','hearings_stats.json')}
Witness org matching uses exact normalized names of whole comma-separated segments (1-3 segments), single-token keys must equal the full LD-2 name
(prevents e.g. "Enterprise" -> Enterprise Holdings). Known residual error: a witness's employer that shares a normalized name with an unrelated LD-2 client.

{COMMON}

Row counts
{table('legislative')}
"""
R['executive']=f"""# Executive-branch layer (built {dclib.NOW()})

Sources
- OIRA EO 12866 meetings, reginfo.gov public calendar (completed meetings 2023-01 .. 2026-11; detail pages with requestor + attendee list + org): `raw/oira_meetings.jsonl`.
  No published meetings appear for Oct 2025 (the calendar returns none for that month).
- White House visitor records (WAVES): the current administration does not publish them. A White House official said in Feb 2025 they would not be released
  during the second Trump term (Washington Examiner report, as cited by Vox Luci on 2026-11-15; logs are Presidential Records until 5 years after the term). Used instead: the Biden White House
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
{stats('executive','executive_stats.json')}

{COMMON}

Row counts
{table('executive')}
"""
R['ethics']=f"""# Ethics layer (built {dclib.NOW()})

Sources
- House Clerk financial disclosure index `<year>FD.zip` (2023-2026) and electronic periodic transaction report PDFs
  (disclosures-clerk.house.gov/public_disc/ptr-pdfs/<year>/<DocID>.pdf), parsed with pdftotext. Paper/scanned PTRs (DocIDs not starting with 2) are listed in
  `raw/house_ptr_docs.jsonl` with status not_electronic and contain no parsed rows.
- Senate eFD (efdsearch.senate.gov): electronic PTRs and annual reports filed 2023-01-01..now by senators. The site requires every visitor to acknowledge its
  statutory notice on use of the reports (no commercial/credit/solicitation use); this research use is non-commercial. Paper filings are recorded, not parsed.
- House privately funded travel ("Gift Travel Filings") XML, disclosures-clerk.house.gov/public_disc/gift-pdfs/<year>Travel.zip, 2023-2026 (members and staff).

Files
- `stock_transactions.csv` House + Senate STOCK Act transactions: member, owner, asset, ticker, type, dates, amount range (min/max), LD-2 org match for the company.
- `edges_member_company_trades.csv` member -> asset (ticker), counts, purchase/sale split, summed range bounds, LD-2 org (company that lobbies).
  Company->LD-2 match: exact normalized name, else the most-filed LD-2 org whose key starts with the company key (prefix_norm, medium).
- `senate_annual_holdings.csv` Senate annual-report Part 3 assets (holdings) with LD-2 org match; `senate_annual_gifts.csv` (Part 5),
  `senate_annual_travel_reimbursements.csv` (Part 6).
- `house_privately_funded_travel.csv` each trip: member office, traveler (member or staff), destination, dates, sponsor, LD-2 org match.
- `edges_travel_sponsor_to_member.csv` sponsor -> member office (n trips, member vs staff trips).
- Gaps: House annual FD holdings/gifts (Schedules A/G/H) are PDFs not parsed here; House gift reports otherwise appear only inside those PDFs.
  Senate privately funded travel (Rule 35 pre-approval forms) is not in eFD as structured data; only annual-report travel reimbursements are included.

Stats
{stats('ethics','ethics_stats.json')}

{COMMON}

Row counts
{table('ethics')}
"""
R['state_events']=f"""# State-level and events layer (built {dclib.NOW()})

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

{COMMON}

Row counts
{table('state_events')}
"""
for d,txt in R.items():
  p=os.path.join(F,d,'README.md'); dclib.keep_prev(p)
  old=open(p).read() if os.path.exists(p) else ''
  log=old[old.find('## Build log'):] if '## Build log' in old else '## Build log (append-only)\n'
  log=log.rstrip()+f"\n- {dclib.NOW()}: rebuilt; counts above.\n"
  open(p,'w').write(txt+'\n'+log)
print('ok')
