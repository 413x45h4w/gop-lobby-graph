# LD-2 layer: full lobbying reports (Senate/House LDA API)

Pulled 2026-11-22 20:08–20:35 ET from `https://lda.gov/api/v1/filings/` (lda.senate.gov now redirects there). There are 297,355 original quarterly LD-2 reports from 2023 Q1 through 2026 Q3. The per-quarter counts match the API `count` exactly (`raw/api_counts_at_crawl.txt`). Each raw record carries its own pull timestamp (`f`). The raw files are `raw/ld2full_<year>_<Q>.jsonl.gz`, 99 MB in total. They are kept on the box but git-ignored. `raw_manifest.csv` holds the sha256, record count and pull window for each file.

Build: `python3 crawl_ld2_full.py <year> <Q>` (resumable through the `.next`/`.done` files), then `fetch_billstatus.py`, then `build_ld2.py`.

## Keys
- **person_id / lda_lobbyist_id**: `person_id` is the merged-person id from `../money_all/people_all.csv`, the all-party universe of 21,408 people. It equals an LDA lobbyist id, and `person_key` lists the merged ids. `in_lobbyist_universe_scored` is True when the LDA id is in `../lobbyist_universe_scored.csv`. 100% of LD-2 lobbyist ids map to a person_id, because that universe was built from the same LD-2 data.
- **client_key**: normalized client name (upper case, punctuation and corporate suffixes such as INC/LLC/CORP/THE/AND removed). LDA `client_id` is per registrant-client pair, so one organization lobbying through 5 firms has 5 ids. `lda_client_ids` lists them.
- **bill_id**: Congress.gov style `hr1234-119`. Types: hr, s, hres, sres, hjres, sjres, hconres, sconres.
- **committee_id**: congress-legislators `thomas_id` (`HSWM`, `SSFI`, or subcommittee `HSWM01`). It is the same id used in `raw/committee-membership-current.yaml`.
- **bioguide**: Congress bioguide id, as used in money_all and x_all.

## Files
| file | rows | what |
|---|---|---|
| ld2_filings.csv.gz | 297,355 | one row per report: registrant, client, income/expenses, issue codes, bills parsed, counts |
| edges_lobbyist_client.csv.gz | 115,216 | lobbyist → (registrant, client): filings, attributed USD (report amount ÷ lobbyists on the report), quarters, issue codes |
| edges_client_bill.csv.gz | 145,246 | client → bill: filings and the summed USD of the reports that mention the bill. Not additive, because one report lists many bills. |
| edges_lobbyist_bill.csv.gz | 606,820 | lobbyist → bill, from the activity lines the lobbyist is listed on |
| edges_lobbyist_agency.csv.gz | 177,780 | lobbyist → government entity contacted (House, Senate, agencies) |
| edges_client_agency.csv.gz | 99,110 | client → government entity |
| edges_bill_committee.csv | 35,683 | bill → committees and subcommittees of referral (GovInfo BILLSTATUS) |
| edges_bill_sponsor_member.csv.gz | 315,609 | bill → sponsor and cosponsors (bioguide) |
| edges_client_committee.csv.gz | 72,871 | client → committee of jurisdiction, through the bills it lobbied |
| edges_client_member_reach.csv.gz | 861,734 | client → current member who sponsored or cosponsored a bill the client lobbied on, plus the member's committees that hold those bills |
| clients.csv / clients_summary.csv | 24,204 | client attributes, and per-client reach: bills, committees, current members reached through committees and through sponsorship |
| bills/bills.csv.gz, bill_committees.csv.gz, bill_sponsors.csv.gz | 35.8k bills | every 118th and 119th Congress bill (BILLSTATUS bulk, pulled 2026-11-22 20:14 ET) |

## Method and confidence
- Bills are regex-parsed from each activity's specific-issue description (`H.R. 1234`, `S. 56`, `H.J.Res. 7` and similar). Congress is inferred from the filing year (2023–24 = 118th, 2025–26 = 119th). That is wrong for a bill cited by number from an earlier Congress. `bill_id_confidence` says whether the text named the Congress explicitly. 145,105 of 145,246 client→bill edges resolve to a real BILLSTATUS bill (`bill_in_billstatus`); the 141 that don't are probable false parses. Only the first number of a list like "H.R. 1, 2, 3" is captured.
- 82,676 of 297,355 reports (28%) name at least one bill. The rest describe issues in prose only.
- Amounts: income for outside firms, expenses for in-house filers. Single income values ≥ $5M are excluded as implausible, the same rule as `money_all/universe_all.py`; they are listed in `build_stats_ld2.json`. In-house expenses are kept at any size (for example the US Chamber's $265.7M).
- "Members reached" through committees is saturated: big multi-issue clients reach almost every member. `n_current_members_sponsor` (distinct current members who *sponsored* a bill the client lobbied) is the more discriminating measure, and `clients_summary.csv` is sorted by it.

## Gaps
- Amended reports (1A–4A), LD-1 registrations, and Q4 2026 (due Jan 20, 2027) were not pulled. Filings before 2023 are not covered here; 2022 Q4 is in `../../lda/ld2_universe`, without descriptions.
- Committee membership is current only, from congress-legislators. Historical rosters were not used.
