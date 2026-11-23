# nonprofits/: dark money (IRS Form 990 e-file and IRS 527 filings)

Built 2026-11-22 ET by `scripts/*.py`. Append-only: rebuilds keep older outputs as `*.prev_<YYYYMMDD_HHMM>.*`. Everything is public IRS data. Gaps are listed at the bottom.

## Sources
- **IRS EO Business Master File** `eo1-4.csv` (https://www.irs.gov/pub/irs-soi/): EIN, name, subsection (c)(3)/(4)/(5)/(6), downloaded 2026-11-22.
- **IRS TEOS e-file 990 XML**: indexes `index_{2024,2025,2026}.csv` and individual returns read by HTTP range requests from the IRS zip batches. Whole zips are never downloaded and XML is not stored.
  - Some 2025/2026 batches use Deflate64, decompressed with `inflate64`.
  - 76 returns listed under batch `2026_TEOS_XML_05A` actually sit in sibling `05B`.
  - Latest e-filed 990, 990EZ or 990PF per EIN (tax years 2022-2025).
- **IRS Political Organization (527) full data file** (POFD `FullDataFile.txt`, transmission 2026-11-21), streamed from raw/irs527_fulldata_20261122.zip (366 MB zip, not committed). It covers Form 8871 notices (with officers) and Form 8872 reports (Sched A contributions, Sched B expenditures).
- ProPublica Nonprofit Explorer was tested, but its API exposes no object ids or officer and grant detail, so IRS XML was used directly.

## Which orgs (`targets_990.csv`, `targets_990_pass2.csv`)
1. **Curated** politically active (c)(3) think tanks, (c)(4)s and (c)(6)s, listed in `scripts/curated_orgs.txt`. Names were resolved to an EIN by exact normalized BMF name, preferring the stated state and then the largest revenue; the `name_match_note` column flags multi-hits.
2. **LDA top-3,000 clients** (2023-26 spend) whose normalized name exactly equals a BMF (c)(3)-(6) org.
3. **Pass 2:** (c)(4)/(5)/(6) grantees receiving at least $100k in pass-1 Schedule I or 990PF grants (517), and BMF orgs among the top super PAC donors (118).

That is 1,535 orgs selected and **1,463 returns parsed**: 588 (c)(4), 483 (c)(6), 339 (c)(3), 53 (c)(5). The other 72 were not parsed: 71 have no e-filed 990 in the 2024-26 indexes, and 1 is a duplicate EIN across passes.

23 curated names did not resolve; see `targets_curated_unresolved.txt`. They include Concord Fund/JCN, Rule of Law Trust, Marble Freedom Trust, Stand With Crypto Alliance, Crypto Council for Innovation, Turning Point Action, SBA Pro-Life America, Arabella Advisors (a for-profit), Indivisible Action, Securing American Greatness, 1776 Action and others. They are absent from the BMF under those names, may file under a different name, or are not e-filed.

## Files
| file | rows | what |
|---|---|---|
| `orgs_990.csv` | 1,463 | one row per org: subsection, revenue, Part IV political/lobbying flags, Schedule C amounts (political expenditures, 527 exempt-function, lobbying, non-deductible dues), LDA client key and spend, mission, IRS source url |
| `edges_person_org_officer.csv` | 41,144 | **person→org officer/director/key-employee edges** (990 Part VII-A, 990EZ, 990PF), with compensation. Matched lobbyist (`lobbyist_person_id`) and member (`member_bioguide`) columns are filled only for accepted matches. |
| `person_match_ambiguous.csv` | 1,510 | name hits not accepted (common names, several candidates, current-member namesakes) |
| `edges_org_to_org_grants.csv` (gitignored; `.csv.gz` committed) | 122,674 | **org→org grants**: Schedule I (and 990PF paid grants) with grantee EIN, BMF subsection, purpose. `quality_flag` marks 26 grants larger than the grantor's total revenue (e.g. NCPA→"CPV" $515M), which are kept but should be excluded. $34.2B in unflagged grants. |
| `edges_org_related_schedR.csv` | 13,285 | Schedule R related organizations (controlled entities, c3↔c4 pairs, partnerships) and related-org transactions |
| `edges_org_to_527_or_committee_schedC.csv` | 2,887 | **org→527/PAC transfers** from Schedule C Part I-C line 5. 282 are matched to an FEC committee id by exact normalized name. |
| `edges_nonprofit_to_superpac_fec.csv` | 512 | **nonprofit→super PAC** contributions from FEC itemized receipts (`outside_money/superpac_top_donors.csv`), matched by exact normalized name |
| `irs527_orgs_totals_2023_26.csv` | 945 | per 527: Sched A receipts and Sched B spending 2023-26 |
| `irs527_contributions_2023_26.csv` (`.csv.gz`) | 197,993 | 527 Sched A rows that are at least $5,000 or matched. `contributor_kind` is one of `person_lobbyist`, `org_lda_client`, `org_nonprofit_target` or `person_employee_of_lda_client`. |
| `irs527_expenditures_2023_26.csv` (`.csv.gz`) | 169,542 | 527 Sched B rows of at least $1,000. 3,629 have recipients matched to an FEC committee id. |
| `irs527_officers_8871.csv` | 31,222 | officers and directors on each active 527's latest Form 8871, with lobbyist and member matches |
| `nonprofits_stats.json`, `irs527_stats.json` | | run statistics |

## Match keys and confidence (`scripts/personmatch.py`)
- Lobbyists → `person_id` (`money_all/people_all.csv`; join `lobbyist_universe_scored.csv` via `people_all.person_key` LDA ids). Names come from LD-2/LD-203 filings with nickname variants.
  - `high_org_link`: the name matches, and the org is one of that lobbyist's 2023-26 LDA clients or registrants (e.g. an association's own in-house lobbyist, or a firm lobbyist on a client's board).
  - `medium_unique`: the only lobbyist with that name, and the surname is uncommon (3 or fewer name keys). There is no org link.
  - Everything else goes to the ambiguous files.
- Members → `bioguide` (congress-legislators current and historical, terms since 1990).
  - `high_title_or_org`: the title or org text says Congress, Senator, U.S. Senate, House of Representatives or former Rep/Sen.
  - `medium_name_former_member`: exact former-member name, uncommon surname. **Spot check: about 75-80% precision.** Real hits include DeMint and Meadows (CPI), Zeldin (RJC), Panetta (CSIS), Kinzinger and Comstock, Fingerhut (JFNA), Bentsen (SIFMA), Matheson (NRECA) and Giffords and Udall. Namesakes include "John Warner" (AHA), "James Clarke" (Hackensack) and "Andrew Jacobs" (IDFA). **Review before drawing.**
  - A bare name match to a *current* member is treated as a namesake (ambiguous file), because sitting members rarely hold such posts.
- Orgs → EIN. LDA clients → `client_key` (normalized name, `boards/scripts/orgnorm.py`). FEC committees → `fec_committee_id`.

## Match rates
- 990 people: 41,144 rows.
  - 1,018 matched to 976 lobbyists (658 high, 360 medium).
  - 87 matched to 78 former members.
  - 1,510 ambiguous.
- 527 Sched A (2.79M rows 2023-26, from 9,513 non-superseded 8872s):
  - 7,077 rows matched to 1,066 lobbyists ($3.34M; 3,387 high, 3,690 medium)
  - 15,532 rows from LDA-client organizations
  - 137,871 rows from employees of LDA clients
- 527 officers: 215 matched to lobbyists, 33 to members.

## Notable
- **(c)(4)→super PAC conduits** (FEC itemized):
  - Future Forward USA Action → FF PAC: $266M (2024)
  - House Majority Forward → HMP: $93.7M (2026) and $47.1M (2024)
  - One Nation → SLF: $70.7M (2026)
  - American Action Network → CLF: $64.3M (2026) and $43.0M (2024)
  - Fund for Policy Reform → Democracy PAC: $60M and $50M
  - Stand Together Chamber of Commerce (c6) → AFP Action: $44.8M
- **Grant chains:**
  - Stand Together Chamber → Americans for Prosperity: $121M
  - Fund for Policy Reform → Open Society Action Fund: $157M
  - New Venture Fund → Sixteen Thirty Fund: $58.9M
  - Future Forward USA Action → America Votes: $34.2M, and → Sixteen Thirty Fund: $27.7M
  - Climate Power → Future Forward USA Action: $25M
  - Tides Foundation → Tides Advocacy: $28.2M
- The trade associations with the most matched lobbyists on their 990 officer and board lists are ITI (26), Global Business Alliance (13), Autos Drive America, the U.S. Chamber, A4A, BPC Action and American Waterways Operators.
- Largest 527s, 2023-26 receipts: ActBlue Non-Federal ($537M, a conduit), DGA ($389M), RGA ($315M), RSLC ($179M), AFSCME Working Families ($98M), RAGA ($93M), DAGA ($91M), DLCC ($89M).

## Gaps
- Only the **latest** return per org was parsed. There is no multi-year history, and 990 data lags 1-2 years (most periods end in 2023-2024).
- Schedule B (donors) is redacted in public 990s, so **c4 donor identities are not available**. Only grants out, transfers to 527s and FEC-visible contributions are captured.
- Grantee matching relies on the reported EIN. Grants without an EIN (`grantee_ein` empty) are linked by name only.
- 527 contributor and recipient matching to FEC committees is exact on normalized names. Many 527 rows are state-level.
- ActBlue Non-Federal and ActBlue Technical Services are conduits. Treat their 527 receipts as pass-through.

## Run log (append-only)
- 2026-11-22 20:10-20:38 ET: first build, with three refinement reruns of the matcher: tightened congressional-context regex, current-member namesake demotion, apostrophe-normalization fix. No earlier versions of these files existed.
