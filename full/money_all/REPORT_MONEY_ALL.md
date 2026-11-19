# All-party lobbyist ↔ Congress money layer (every registered lobbyist × every current member)
Generated 2026-11-18 07:29 PM ET (UTC-0500). Folder: full/money_all/. The GOP-only outputs in full/ were not modified; full/x_all/ (daily X job) was not touched.

## Universe
- **Lobbyists: 21,408 people** (22,158 LDA lobbyist IDs; 701 multi-ID people merged). Every lobbyist ID on any LD-2 quarterly report 2023Q1–2026Q3 (297,217 filings, outside firms *and* in-house registrants), plus 1,358 people who filed an LD-203 (2023 mid-year – 2026 mid-year) but appear on no 2023+ LD-2.
  - Kinds: in-house 10,989 · outside firm 7,976 · both 158 · LD-2 with no amount reported (<$5K) 927 · LD-203 only 1,358.
  - Merge rule (extends full/merge_people.py): same canonical name (nickname→formal first name + last name, middle names and suffixes ignored) AND (covered-position Jaccard ≥0.4 OR registrants share first word OR share a distinctive word (in ≤25 registrant names) OR the IDs' LD-203s list ≥3 identical items).
  - Lobbying dollars = LD-2 income (outside firms) or expenses (in-house) split equally among the filing's lobbyists (heuristic, as before). 6 LD-2 filings by LOC COMMUNITY ASSOCIATION reporting $20M/quarter are treated as implausible and excluded (income_outliers_excluded.csv).
- **Members: 539 current members** (legislators-current.json fetched 2026-11-17): House 221 R / 217 D / 1 I, Senate 53 R / 45 D / 2 I (includes the 6 non-voting delegates). FEC committees found for 538; Sen. Alan Armstrong (R-OK, appointed 2026-03-24) has no FEC candidate ID, so he can only receive LD-203 edges. Sen. Darline Graham's FEC ID (S6SC04437) was added by an exact cn26 name+state+office match.
- Member committees: 1,212 (672 principal/authorized/JFC from FEC bulk ccl24+ccl26 dated 2026-11-18; 540 leadership PACs from OpenFEC sponsor_candidate_id) — bundling/member_committees_all.csv.

## Layers (edges, dollars by recipient party)
"Scored" = the same crediting rules as the GOP build: each item capped at $7,000; LD-203 party-committee payees ×0.5; LD-203 PAC-sourced items ×0.5; FEC memo rows and low-confidence matches excluded; LD-203 items duplicating an FEC row (same person, member, amount, ±3 days) dropped in favour of FEC; FEC rows to party committees (type X/Y/Z) excluded (3,203 rows, $6.20M raw).

| Layer | Edges | Lobbyists | Members | Raw $ R / D / I | Scored $ R / D / I |
|-|-|-|-|-|-|
| 1. LD-203 contributions | 114,879 member-matched items; 62,688 after FEC de-dup (39,209 pairs) | 5,502 | 533 | $57.48M / $33.52M / $0.14M | $42.91M / $24.72M / $0.11M |
| 2. FEC individual contributions | 72,901 scored rows (68,760 high, 4,141 medium; 42,375 pairs) | 5,795 | 536 | $41.51M / $30.31M / $0.14M | $41.20M / $30.31M / $0.14M |
| 3. Former employer (covered position) | 2,083 edges | 1,648 | 387 | 1,071 R / 997 D / 15 I edges | (count layer) |
| 4. Form 3L bundling | 175 committee×bundler×half-year rows | 6 registrant PACs (credited to 89 of their lobbyists, split equally) | 60 (59 D, 1 R) | $23.33M total: D $23.03M / R $0.30M | same |
| **Combined pairs (1+2+3)** | **71,803 pairs** (70,165 with $) | **7,242 with $** | **538** | | **$139.39M: R $84.11M / D $55.03M / I $0.25M** |

- FEC leadership-PAC rows (7,447 scored) are included here; the GOP build matched principal/authorized committees only.
- **Bundling detail:** every member-committee Form 3L line is a registrant PAC, not an individual lobbyist: AIPAC PAC $21.42M (D $21.12M, R $0.30M – Messmer), J Street PAC $1.53M, National Association of Realtors $246K, Mortgage Bankers $62.5K, LCV Action Fund $36.5K, NAB $33K. $0 of individual-lobbyist bundling to any current member. Top recipients: Wesley Bell $5.46M, Jacky Rosen $1.83M, Josh Gottheimer $1.63M, Don Davis $1.55M, Jared Golden $0.82M. Non-member context (Trump committees, DCCC, etc.) matched to universe people: $82.5M (bundling/bundling_matched_nonmember_committees_context.csv, not scored).
- Org PAC → registrant resolution is per FEC PAC ID (connected-org name, committee name, and every reported spelling): bundling/org_bundler_resolution.csv. Unresolved: Rocket PAC, Club for Growth PAC (no LDA registrant match).

## Score and party lean
- Money score (same v2 weights, percentiles over all 21,408): 0.315 lobbying $ + 0.315 $ to members + 0.18 members funded + 0.09 former-employer members + 0.10 Form 3L bundling.
- **party_lean** per lobbyist: from $ to current members (R share ≥0.67 → R, ≤0.33 → D, else mixed; needs ≥$2,000; Independents counted with D); if no member giving, from all LD-203 FECA giving incl. party committees; else from covered-position lean (legislators/party keywords named in covered positions). Columns usd_to_R/D/I_members, member_giving_R_share, ld203_all_feca_R_share, covered_position_lean are all kept. Lean counts: R 3,748 · D 2,953 · mixed 500 · unknown 14,207 (mostly in-house staff with no giving and no Hill history).

### Top 25 overall
|#|Lobbyist|Firm|Kind|Lobbying $ 2023-26|$ to members|Members funded|R share of member $|Covered-position lean|Party lean|Former employer|Score|GOP-300 rank|
|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|Sam Olswanger|Akin Gump Strauss Hauer & Feld|outside|$10.3M|$306,150|63|1.0|R|R|Daniel Webster (R), Marsha Blackburn (R)|94.66|1|
|2|Jeff Bjornstad|Washington2 Advocates|outside|$7.1M|$144,182|67|0.178|D|D|Adam Smith (D), Patty Murray (D), Rick Larsen (D)|94.35|-|
|3|Jose Borjon|Akin Gump Strauss Hauer & Feld|outside|$10.8M|$154,875|63|0.0|D|D|Henry Cuellar (D)|94.16|-|
|4|Erskine Wells|Bgr Government Affairs|outside|$7.6M|$172,100|58|1.0|R|R|Roger F. Wicker (R)|94.03|16|
|5|Monica Popp|Marshall & Popp, Llc|outside|$7.8M|$193,774|49|1.0|R|R|John Cornyn (R)|94.01|10|
|6|Sudafi Henry|Thegroup Dc, Llc|outside|$5.9M|$176,088|48|0.0|D|D|Emanuel Cleaver (D), Steny H. Hoyer (D)|93.99|-|
|7|Mike Mckay|Empire Consulting Group|outside|$6.1M|$304,708|67|0.0|D|D|Gregory W. Meeks (D)|93.95|-|
|8|Anne Macmillan|Invariant Llc|outside|$7.3M|$122,067|74|0.0|D|D|Nancy Pelosi (D)|93.93|-|
|9|Daniel Farmer|Bgr Government Affairs|outside|$7.7M|$116,383|50|0.004|D|D|Debbie Wasserman Schultz (D)|93.8|-|
|10|Remy Mason|Bgr Government Affairs|outside|$7.2M|$71,250|52|0.0|D|D|Elizabeth Warren (D), Patty Murray (D)|93.75|-|
|11|Hazen Marshall|Marshall & Popp, Llc|outside|$7.9M|$121,900|38|1.0|R|R|Mitch McConnell (R)|93.72|26|
|12|Nadeam Elshami|Brownstein Hyatt Farber Schreck, Llp|outside|$8.1M|$57,000|43|0.0|D|D|Janice D. Schakowsky (D), Nancy Pelosi (D), Richard J. Durbin (D)|93.61|-|
|13|Jane Lucas|Alston & Bird Llp|outside|$7.1M|$98,250|42|1.0|R|R|John Thune (R)|93.55|37|
|14|Syd Terry|Bgr Government Affairs|outside|$4.8M|$107,191|65|0.009|D|D|Janice D. Schakowsky (D), Mark Pocan (D)|93.49|-|
|15|Charles French|Cozen O'Connor Public Strategies|outside|$6.5M|$79,916|58|0.404|R|mixed|Pete Sessions (R)|93.45|114|
|16|Katie Schoettler|Foley & Lardner Llp|outside|$4.6M|$237,750|167|0.534|R|mixed|Steve Daines (R)|93.43|83|
|17|Mark Warren|Brownstein Hyatt Farber Schreck, Llp|outside_and_in_house|$7.7M|$69,750|51|1.0|R|R|John Thune (R)|93.43|35|
|18|Ann Jablon|Capitol Counsel Llc|outside|$7.1M|$81,025|44|0.0|D|D|Richard E. Neal (D)|93.41|-|
|19|Jeffrey Carroll|Capitol Counsel Llc|outside|$6.7M|$78,750|46|0.0|D|D|Frank Pallone, Jr. (D)|93.37|-|
|20|Jonathan Hiler|Miller Strategies, Llc|outside|$11.7M|$67,000|34|0.985|R|R|Tom Cotton (R)|93.35|34|
|21|Michael Higdon|A1.9 Strategies Llc|outside|$6.7M|$109,300|28|1.0|R|R|Harold Rogers (R)|93.32|45|
|22|Matt Bravo|S-3 Group|outside_and_in_house|$7.6M|$110,650|24|1.0|R|R|Steve Scalise (R)|93.31|50|
|23|Landon Stropko|Invariant Llc|outside|$6.0M|$96,200|41|1.0|R|R|Cynthia M. Lummis (R)|93.29|59|
|24|David Thomas|Mehlman Consulting, Inc.|outside|$4.8M|$116,839|74|0.0|D|D|Zoe Lofgren (D)|93.23|-|
|25|Jerr Rosenbaum|Penn Avenue Partners|outside|$6.2M|$105,342|30|1.0|R|R|John Cornyn (R)|93.22|60|

### Top 10 Republican-lean
|#|Lobbyist|Firm|Kind|Lobbying $ 2023-26|$ to members|Members funded|R share of member $|Covered-position lean|Party lean|Former employer|Score|GOP-300 rank|
|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1|Sam Olswanger|Akin Gump Strauss Hauer & Feld|outside|$10.3M|$306,150|63|1.0|R|R|Daniel Webster (R), Marsha Blackburn (R)|94.66|1|
|4|Erskine Wells|Bgr Government Affairs|outside|$7.6M|$172,100|58|1.0|R|R|Roger F. Wicker (R)|94.03|16|
|5|Monica Popp|Marshall & Popp, Llc|outside|$7.8M|$193,774|49|1.0|R|R|John Cornyn (R)|94.01|10|
|11|Hazen Marshall|Marshall & Popp, Llc|outside|$7.9M|$121,900|38|1.0|R|R|Mitch McConnell (R)|93.72|26|
|13|Jane Lucas|Alston & Bird Llp|outside|$7.1M|$98,250|42|1.0|R|R|John Thune (R)|93.55|37|
|17|Mark Warren|Brownstein Hyatt Farber Schreck, Llp|outside_and_in_house|$7.7M|$69,750|51|1.0|R|R|John Thune (R)|93.43|35|
|20|Jonathan Hiler|Miller Strategies, Llc|outside|$11.7M|$67,000|34|0.985|R|R|Tom Cotton (R)|93.35|34|
|21|Michael Higdon|A1.9 Strategies Llc|outside|$6.7M|$109,300|28|1.0|R|R|Harold Rogers (R)|93.32|45|
|22|Matt Bravo|S-3 Group|outside_and_in_house|$7.6M|$110,650|24|1.0|R|R|Steve Scalise (R)|93.31|50|
|23|Landon Stropko|Invariant Llc|outside|$6.0M|$96,200|41|1.0|R|R|Cynthia M. Lummis (R)|93.29|59|

### Top 10 Democratic-lean
|#|Lobbyist|Firm|Kind|Lobbying $ 2023-26|$ to members|Members funded|R share of member $|Covered-position lean|Party lean|Former employer|Score|GOP-300 rank|
|-|-|-|-|-|-|-|-|-|-|-|-|-|
|2|Jeff Bjornstad|Washington2 Advocates|outside|$7.1M|$144,182|67|0.178|D|D|Adam Smith (D), Patty Murray (D), Rick Larsen (D)|94.35|-|
|3|Jose Borjon|Akin Gump Strauss Hauer & Feld|outside|$10.8M|$154,875|63|0.0|D|D|Henry Cuellar (D)|94.16|-|
|6|Sudafi Henry|Thegroup Dc, Llc|outside|$5.9M|$176,088|48|0.0|D|D|Emanuel Cleaver (D), Steny H. Hoyer (D)|93.99|-|
|7|Mike Mckay|Empire Consulting Group|outside|$6.1M|$304,708|67|0.0|D|D|Gregory W. Meeks (D)|93.95|-|
|8|Anne Macmillan|Invariant Llc|outside|$7.3M|$122,067|74|0.0|D|D|Nancy Pelosi (D)|93.93|-|
|9|Daniel Farmer|Bgr Government Affairs|outside|$7.7M|$116,383|50|0.004|D|D|Debbie Wasserman Schultz (D)|93.8|-|
|10|Remy Mason|Bgr Government Affairs|outside|$7.2M|$71,250|52|0.0|D|D|Elizabeth Warren (D), Patty Murray (D)|93.75|-|
|12|Nadeam Elshami|Brownstein Hyatt Farber Schreck, Llp|outside|$8.1M|$57,000|43|0.0|D|D|Janice D. Schakowsky (D), Nancy Pelosi (D), Richard J. Durbin (D)|93.61|-|
|14|Syd Terry|Bgr Government Affairs|outside|$4.8M|$107,191|65|0.009|D|D|Janice D. Schakowsky (D), Mark Pocan (D)|93.49|-|
|18|Ann Jablon|Capitol Counsel Llc|outside|$7.1M|$81,025|44|0.0|D|D|Richard E. Neal (D)|93.41|-|

### Top 10 by dollars to members (regardless of score)
|#|Lobbyist|Firm|Kind|Lobbying $ 2023-26|$ to members|Members funded|R share of member $|Covered-position lean|Party lean|Former employer|Score|GOP-300 rank|
|-|-|-|-|-|-|-|-|-|-|-|-|-|
|1788|Roslyn Brooks|Pwc Us Group Llp|in_house|$1.0M|$863,250|204|0.555|none|mixed|-|80.3|-|
|1337|Roslyn Brooks|Pricewaterhousecoopers|in_house|$1.3M|$808,750|205|0.513|none|mixed|-|82.56|-|
|837|Jeffrey Kimbell|Jeffrey J. Kimbell & Associates, Inc.|outside|$2.0M|$803,350|116|1.0|none|R|-|85.23|-|
|161|Alexander Silbey|Ats Communications, Inc. (Dba Silbey Str|outside|$7.1M|$720,699|76|0.664|D|mixed|-|89.81|-|
|136|Jeffrey Miller|Miller Strategies, Llc|outside|$48.0M|$585,900|103|0.991|none|R|-|90.09|2|
|424|Travis Johnson|1607 Strategies, Llc|outside|$3.3M|$559,875|87|1.0|R|R|-|87.83|-|
|146|Richard Gold|Holland & Knight Llp|outside|$7.8M|$557,159|280|0.485|none|mixed|-|89.94|-|
|150|Norman Brownstein|Brownstein Hyatt Farber Schreck, Llp|outside|$8.0M|$556,335|74|0.614|none|mixed|-|89.89|-|
|854|Van Hipp|American Defense International|outside|$2.0M|$490,400|127|0.841|none|R|-|85.16|-|
|151|John Scofield|S-3 Group|outside|$7.6M|$485,600|93|0.953|R|R|-|89.88|9|

### Top 20 members by scored lobbyist money
|#|Member|Party|Chamber|State|Scored lobbyist $|Lobbyists giving|Form 3L bundled $|Former staff now lobbyists|Top lobbyist donors|
|-|-|-|-|-|-|-|-|-|-|
|1|Jason Smith|R|House|MO|$1,961,004|452|$0|7|Brian Henneberry $30600, William Walters $26500, David Olander $24000, Jeff Mcmillen $22600, Kirsten Chadwick $21000|
|2|Steve Scalise|R|House|LA|$1,785,056|267|$0|25|Martin Reiser $60000, Van Hipp $52000, Brian Henneberry $42000, Matt Bravo $40000, Michael Chappell $36000|
|3|Brett Guthrie|R|House|KY|$1,632,958|510|$0|5|Dean Rosen $31205, Travis Johnson $25000, Ansley Erdel $24000, Adam Buckalew $24000, Amy Jensen $23300|
|4|Mike Johnson|R|House|LA|$1,618,457|290|$0|7|Jeffrey Miller $42000, Brian Henneberry $35000, Ralph Hellmann $34750, Kirsten Chadwick $32500, Scott Dacey $30000|
|5|Ken Calvert|R|House|CA|$1,565,536|449|$0|6|Neely Silbey $47200, Alexander Silbey $40200, Ed Boquist $35250, Letitia White $34600, Harry Glenn $24200|
|6|Tom Emmer|R|House|MN|$1,422,071|341|$0|7|Oswaldo Palomo $30000, Nicholas Uehlecke $29748, John Scofield $22000, W Stephens $21500, Frank Mccarthy $21000|
|7|Tom Cole|R|House|OK|$1,374,079|387|$0|9|Christopher Caron $50900, Alexander Silbey $44200, Neely Silbey $38900, Letitia White $36600, Pete Kirkham $33600|
|8|Frank Pallone, Jr.|D|House|NJ|$1,312,563|343|$0|10|Michael Merola $40900, Melanie Nathanson $34550, Lauren Aronson $30120, Karissa Willhite $26300, Kate Rose $26100|
|9|Martin Heinrich|D|Senate|NM|$1,308,393|479|$35,395|8|Kai Anderson $21000, Melanie Nathanson $19300, Richard Gold $18000, Joseph Britton $17700, Alexander Mcdonough $17000|
|10|Mark R. Warner|D|Senate|VA|$1,287,018|538|$722,856|15|John Simmons $22800, Brian Pomper $20550, John Raffaelli $19800, Alan Rosenbloom $16250, Peter Jacoby $16000|
|11|John Thune|R|Senate|SD|$1,262,196|353|$0|17|Dustin Marquis $31600, Jeffrey Kimbell $30000, Travis Johnson $25000, Robert Chamberlin $23500, Brian Henneberry $21000|
|12|Katherine M. Clark|D|House|MA|$1,183,243|410|$680,784|4|Michael Williams $29500, Sudafi Henry $23400, Rebecca Gould $20500, Lori Denham $18800, Karissa Willhite $18800|
|13|Maria Cantwell|D|Senate|WA|$1,148,674|491|$0|16|Norman Brownstein $19400, Richard Sullivan $16500, Samuel Whitehorn $13600, Jonathan Lamy $13200, Jeff Bjornstad $13200|
|14|Thom Tillis|R|Senate|NC|$1,146,221|359|$0|14|Daniel Todd $21300, Andrew Woods $20000, Tyler Deaton $17800, Raissa Downs $17200, Jeffrey Kimbell $17200|
|15|John Barrasso|R|Senate|WY|$1,128,603|358|$0|8|David Bridges $25900, Brendan Dunn $25600, Bryan Cunningham $24150, Jeffrey Kimbell $20000, Marne Marotta $19750|
|16|J. French Hill|R|House|AR|$1,127,610|324|$0|0|Warren Tryon $29800, Kara Calvert Cambell $29300, Justin Daly $27600, Leonard Wolfson $21000, Travis Johnson $20000|
|17|Hakeem S. Jeffries|D|House|NY|$1,118,844|373|$0|5|Thomas Kahn $46000, Mike Mckay $31100, Sudafi Henry $30200, Darrel Thompson $28200, Norman Brownstein $22000|
|18|Mike Rogers|R|House|AL|$1,070,696|406|$0|0|Josh Holly $50262, Van Hipp $44600, Michael Herson $32500, Letitia White $20400, Carl Kime $20000|
|19|John Cornyn|R|Senate|TX|$1,068,080|390|$0|25|Matthew Johnson $24900, John Martin $21787, Monica Popp $21250, Russell Thomasson $20000, Amy Jensen $18000|
|20|Roger F. Wicker|R|Senate|MS|$1,039,854|397|$0|20|Susan Sweat $35600, Charles Rathburn $24650, Anthony Lazarski $22400, Denise Bode $19500, Dana Wood $18950|

## False-positive safeguards (rejected/ambiguous files)
- **fec_ambiguous_all.csv (4,064 rows):** several same-name LDA people tie at the best evidence tier, or best evidence is only medium/low with ≥2 same-name people, or the donor's occupation is lobbying but the employer is a *different* LDA registrant. Employer→registrant matching uses only distinctive registrant words (≤25 registrant names), so words like AMERICAN/NATIONAL/ASSOCIATION cannot create a high match. 8,117 low-confidence rows (name + DC-area professional) are in edges_fec_all.csv but not scored. 369,049 name hits were rejected for having no employer/occupation evidence.
  - Check against the GOP build: 97% of the old 300's scored FEC sub_ids are reproduced; ~330 old rows are now ambiguous because a same-name lobbyist exists elsewhere in the full universe.
- **ld203_rejected_name_matches.csv (668 items):** surname-only honoree matches rejected because the surname is preceded by a conflicting given name (e.g. "Markwayne Mullin" ≠ Rep. Kevin Mullin; "Will Hurd" ≠ Rep. Jeff Hurd; "Janet Mills" ≠ Rep. Cory Mills). This bug existed in the GOP matcher but was masked there because most mis-hits pointed at Democrats.
- **former_employer_rejected_all.csv (296):** ambiguous legislator names (253, e.g. two current Mike Rogers; "Bob Matsui"), and covered-position segments that are lists of ≥3 legislators with no staff-role word (43, contact lists, not jobs).

## Caveats
- **Income attribution** (equal split per filing) and **in-house expenses** (whole-organisation lobbying spend, which can include fees paid to outside firms) are heuristics; in-house and outside dollars are combined in one percentile.
- **PAC administrators:** LD-203 items where the contributor is the employer's PAC (e.g. Roslyn Brooks/PwC PAC, $0.8M under each of two LDA IDs) are counted at 0.5, as before, but still put PAC treasurers high on "$ to members". Her two IDs (PricewaterhouseCoopers / PwC US Group) are not merged by the rule.
- **Top of the ranking is compressed** (scores 93–95): income and $ percentiles are near 1 for all of them, so the binary-ish former-employer term often decides the order. The GOP #2–#5 (Jeffrey Miller, Willcox, Green, Edattel) fall to ~#136–147 here because they have no covered-position ties to current members, not because their giving dropped (Miller: $585,900 to 103 members, the 5th-highest $ total).
- **Bundling** credits org-PAC bundling to every lobbyist of that registrant (split equally), as in the GOP build; AIPAC's $21.4M dominates. Form 3L exists only above the threshold and when the committee chooses to report, so absence ≠ no bundling. 5 Form 3L filings were missing from the OpenFEC cycle listing (pagination duplicates) and were recovered from the per-committee all-time query.
- **Name matching** is name-based throughout (no biometric or other identity inference). LD-203 honoree "unique_last" matches (4,728 items) are the weakest LD-203 tier.
- **Not covered:** registrant-filed LD-203s (organisation PAC reports) are excluded, as in the GOP build; LD-2 amendments not reconciled; lobbyists active only before 2023 excluded; Alan Armstrong has no FEC committee; leadership PAC lookup for the manually added Darline Graham ID was not re-queried.
- FEC bulk files: indiv24/indiv26 dated 2026-11-15 (FEC update), ccl/cm/cn dated 2026-11-18. OpenFEC calls: 52 this run, all logged with api_key=REDACTED in bundling/api_calls.log.

## Files
- Universe: people_all.csv, lobbyist_ids_all.csv, income_outliers_excluded.csv
- Edges: edges_ld203_all.csv(.gz) (raw member-matched items), edges_ld203_all_dedup.csv(.gz) (with dup_of_fec_sub_id), edges_fec_all.csv(.gz), edges_former_employer_all.csv, edges_bundling_all.csv, edges_money_pairs_all.csv(.gz)
- Rejected/ambiguous: fec_ambiguous_all.csv, ld203_rejected_name_matches.csv, former_employer_rejected_all.csv, bundling/bundling_ambiguous_or_low.csv
- Rankings: ranking_money_all.csv (party_lean, rank_within_R_lean / rank_within_D_lean, gop300_prev_money_rank), member_totals_all.csv
- Charts: ranking_money_all_top25.png, network_top50_all.png, member_totals_top25.png
- Stats: build_stats_all.json, fec_match_stats.json, bundling/bundling_summary_all.json
- Scripts (run order): universe_all.py → ld203_edges_all.py → fec_pass_all.py 24/26 → fec_match_all.py → bundling/member_committees_all.py → bundling/pull_f3l_all.py → bundling/parse_aggregate_all.py → build_money_all.py → plots_all.py. Outputs are copied to *.prev_<timestamp>.* before being overwritten (safeio.py).
- Raw, not in git: raw/fec_bulk/indiv24.zip (4.2 GB) and indiv26.zip (2.6 GB). The filtered pulls raw/fec_indiv{24,26}_allmember_poolname.jsonl.gz are committed.
- *.prev_20261118_HHMM.* files are earlier passes of this same build, kept per the append-only rule: a .prev_<HHMM> file is the version that existed just before the pass started at HHMM ET overwrote it. Passes before 19:28 predate the LD-203 given-name safeguard, the former-employer safeguards and/or the LD-203-item merge rule; only the un-suffixed files are final.

## PAC layer (added 2026-11-18 09:13 PM ET (UTC-0500))

This layer adds money that reaches members through PACs, party committees and joint fundraising committees (JFCs). It is on top of the direct layer above, not merged into it. The direct-only score is unchanged in method; it was rebuilt once after a name-matching fix (see caveats).

### Sub-layers

1. **Lobbyist → committee** (`edges_lobbyist_to_pac_all.csv`). Every itemized FEC contribution (indiv24/26) by a universe lobbyist to a non-candidate committee: PACs, super PACs, party committees, JFCs and leadership PACs. It also includes LD-203 self-reported items whose payee resolves to an FEC committee and that don't duplicate an FEC row within ±3 days. ActBlue and WinRed conduit rows are excluded. 171,611 rows (164,081 FEC + 7,530 LD-203) from 8,523 lobbyists to 2,598 committees, $88.74M. By committee lean: R $39.33M, D $27.86M, mixed $19.84M, unknown $1.71M. Unresolved LD-203 payees (kept in `pac/lobbyist_to_pac_ld203_unresolved.csv`, not scored): 11,988 rows, $9.89M. Ambiguous FEC name matches are in `pac/lobbyist_to_pac_fec_ambiguous.csv`.
2. **Committee → member** (`edges_pac_to_member_all.csv`, from FEC pas2 2023-26). Direct contributions (24K/24Z): R $439.81M, D $361.26M, I $2.65M. Independent expenditures and party spending are kept as separate categories with their support/oppose flag (member party shown is the member the spending was about). IE support: R $373.44M, D $235.09M, I $1.52M. IE oppose: R $603.58M, D $423.10M, I $1.34M. Party coordinated: R $85.30M, D $46.73M. There are 5,483 committees in total.
3. **Indirect lobbyist → committee → member, pro rata** (`edges_indirect_lobbyist_pac_member.csv`, `pac/indirect_shares_by_lobbyist_pac_cycle.csv`). For each lobbyist, committee and cycle: share = min(1, lobbyist $ ÷ committee total receipts in the FEC webk summary). The lobbyist is then credited share × the committee's direct contributions to each member, excluding the committee's own member. IE support/oppose is attributed the same way but kept in separate columns that are not scored. JFCs give through transfers rather than contributions. For those, the credit is share × the JFC's transfers to each member's committees, from OpenFEC schedule_b by_recipient_id (`edges_lobbyist_jfc_split_to_member.csv`); 508 JFCs had transfer data. Totals: 822,131 lobbyist-member pairs. Via PAC contributions: R $9.84M, D $6.24M, I $0.06M. Via JFC transfers: R $5.93M, D $3.13M, I $0.00M. IE attributed, support: D $0.16M, R $0.06M, I $0.00M. IE attributed, oppose: R $0.55M, D $0.48M, I $0.00M.
4. **Registrant-filed LD-203s** (`edges_registrant_ld203_to_member.csv`). These are the contribution reports filed by the organization rather than an individual lobbyist; they are mostly the organization's PAC giving. Here, 2,202 registrants reported 302,093 items to 536 members. Raw totals: R $396.62M, D $307.38M, I $2.29M. Each item is capped at $7K before crediting, giving: R $388.55M, D $304.79M, I $2.28M. Each registrant's capped total is split equally among its LD-2 lobbyists (9,707 credited), the same linkage used for bundling. This overlaps with sub-layer 2 when the registrant's PAC is in pas2, so it is kept as its own score component and not added to member dollar totals.
5. **Lobbyists who are PAC officers** (`edges_lobbyist_pac_officer.csv`). A lobbyist's name matched the committee's treasurer (FEC cm), custodian of records, or designated agent (Form 1 via OpenFEC, 1,148 committees fetched), AND the committee name or its connected organisation shares a distinctive word with the lobbyist's registrant. That gives 796 edges, 669 lobbyists and 614 committees. By role: treasurer(fec_cm_bulk) 456, custodian_of_records(form1) 140, designated_agent(form1) 200. Name matches without that registrant corroboration are kept unscored in `pac/pac_officer_ambiguous.csv` (1,083 rows).

### Scores

- `direct_only_score` is the existing money score: 0.315 pct(lobbying $) + 0.315 pct($ to members) + 0.18 pct(members funded) + 0.09 pct(former-employer members) + 0.10 pct(bundling).
- `pac_score` = 100 × [0.35 pct(lobbyist $ to committees) + 0.35 pct(indirect pro-rata $ via PACs + JFCs) + 0.15 pct(registrant LD-203 split $) + 0.15 pct(PAC officer roles)].
- `direct_plus_pac_score` = 0.75 × direct_only_score + 0.25 × pac_score. Files: `ranking_money_all_with_pac.csv` and `member_totals_all_with_pac.csv`. Members are ranked by direct lobbyist $ + indirect $ via PACs and JFCs.

### Top committees funded by universe lobbyists

| # | committee | class | lean | $ from lobbyists | lobbyists |
|---|---|---|---|---|---|
| 1 | NRSC | party_national_committee | R | $7.70M | 498 |
| 2 | DSCC | party_national_committee | D | $6.55M | 637 |
| 3 | DCCC | party_national_committee | D | $3.78M | 508 |
| 4 | REPUBLICAN NATIONAL COMMITTEE | party_national_committee | R | $2.77M | 59 |
| 5 | NRCC | party_national_committee | R | $2.18M | 302 |
| 6 | HARRIS VICTORY FUND | joint_fundraising_committee | D | $1.44M | 645 |
| 7 | JOHNSON LEADERSHIP FUND | joint_fundraising_committee | R | $1.27M | 137 |
| 8 | MCCARTHY VICTORY FUND | joint_fundraising_committee | R | $1.04M | 138 |
| 9 | TRUMP 47 COMMITTEE, INC. | joint_fundraising_committee | R | $0.99M | 129 |
| 10 | BHFS-E, PC PAC (BROWNSTEIN HYATT FARBER SCHRECK POLITICAL ACTION COMMITTEE) | corporate_pac | mixed | $0.84M | 85 |
| 11 | DNC SERVICES CORP / DEMOCRATIC NATIONAL COMMITTEE | party_national_committee | D | $0.75M | 357 |
| 12 | GROW THE MAJORITY | joint_fundraising_committee | R | $0.54M | 39 |
| 13 | EQUALITY PAC | hybrid_pac | D | $0.53M | 170 |
| 14 | AKIN GUMP STRAUSS HAUER & FELD LLP CIVIC ACTION COMMITTEE (AKA AKIN GUMP PAC) | nonconnected_pac | mixed | $0.53M | 64 |
| 15 | COOPER VICTORY FUND | joint_fundraising_committee | D | $0.51M | 288 |

### Top 15 lobbyists, direct + PAC score

| # | lobbyist | firm | lean | direct+PAC | direct-only rank | $ to committees | indirect $ | officer roles |
|---|---|---|---|---|---|---|---|---|
| 1 | Ted Lehman | TODD STRATEGY GROUP | R | 93.57 | 40 | $49,625 | $9,786 | 1 |
| 2 | Shawn Donilon | NATIONAL ASSOCIATION OF BROADCASTERS | R | 93.23 | 69 | $28,500 | $8,966 | 1 |
| 3 | Sam Olswanger | AKIN GUMP STRAUSS HAUER & FELD | R | 92.8 | 1 | $71,444 | $38,336 | 0 |
| 4 | Leslie Belcher | STEPTOE LLP | mixed | 92.4 | 26 | $44,262 | $5,029 | 1 |
| 5 | Erskine Wells | BGR GOVERNMENT AFFAIRS | R | 92.11 | 4 | $159,575 | $22,229 | 0 |
| 6 | Nadeam Elshami | BROWNSTEIN HYATT FARBER SCHRECK, LLP | D | 92.07 | 12 | $71,220 | $19,411 | 0 |
| 7 | Jose Borjon | AKIN GUMP STRAUSS HAUER & FELD | D | 91.86 | 3 | $25,091 | $7,397 | 0 |
| 8 | Mark Warren | BROWNSTEIN HYATT FARBER SCHRECK, LLP | R | 91.81 | 17 | $36,140 | $17,539 | 0 |
| 9 | Jane Lucas | ALSTON & BIRD LLP | R | 91.76 | 13 | $42,938 | $14,019 | 0 |
| 10 | Daniel Farmer | BGR GOVERNMENT AFFAIRS | D | 91.63 | 9 | $59,975 | $9,372 | 0 |
| 11 | Remy Mason | BGR GOVERNMENT AFFAIRS | D | 91.6 | 10 | $69,247 | $9,231 | 0 |
| 12 | Andrew Usyk | BROWNSTEIN HYATT FARBER SCHRECK, LLP | D | 91.59 | 33 | $51,270 | $18,382 | 0 |
| 13 | Joseph Lai | BGR GOVERNMENT AFFAIRS | R | 91.48 | 28 | $176,650 | $24,121 | 0 |
| 14 | William Walters | SELECT MEDICAL HOLDINGS CORPORATION | R | 91.38 | 180 | $22,000 | $8,067 | 1 |
| 15 | Jonathan Heafitz | PHARMACEUTICAL CARE MANAGEMENT ASSOCIATION | R | 91.34 | 156 | $52,995 | $16,764 | 2 |

### Top 10 members, lobbyist $ including indirect PAC/JFC $

| # | member | direct lobbyist $ | indirect via PAC | indirect via JFC | all-PAC direct $ (pas2) | IE for / against |
|---|---|---|---|---|---|---|
| 1 | Jason Smith (R-MO) | $1.96M | $0.16M | $0.00M | $6.67M | $0.00M / $0.00M |
| 2 | Mike Johnson (R-LA) | $1.62M | $0.12M | $0.26M | $4.78M | $0.00M / $0.15M |
| 3 | Steve Scalise (R-LA) | $1.79M | $0.08M | $0.02M | $3.73M | $0.00M / $0.00M |
| 4 | Brett Guthrie (R-KY) | $1.63M | $0.20M | $0.06M | $5.72M | $0.08M / $0.00M |
| 5 | Mark R. Warner (D-VA) | $1.29M | $0.09M | $0.35M | $3.12M | $0.01M / $0.00M |
| 6 | Ken Calvert (R-CA) | $1.57M | $0.09M | $0.03M | $3.50M | $1.76M / $7.77M |
| 7 | Katherine M. Clark (D-MA) | $1.18M | $0.10M | $0.38M | $4.39M | $0.00M / $0.00M |
| 8 | Tom Emmer (R-MN) | $1.42M | $0.12M | $0.08M | $5.01M | $0.00M / $0.00M |
| 9 | Dan Sullivan (R-AK) | $0.76M | $0.08M | $0.77M | $2.80M | $6.15M / $15.63M |
| 10 | Tom Cole (R-OK) | $1.37M | $0.12M | $0.00M | $4.24M | $0.52M / $0.00M |

### Caveats

- Pro-rata attribution is a heuristic. Money is fungible, and receipts in the denominator include transfers and non-itemized money, so indirect dollars are an estimate of influence, not a traced flow.
- Lobbyist money to candidate committees that later transfer onward is not passed through, because candidate committees have no webk receipts row.
- JFC party lean: where the pas2/party classifier left a JFC unknown or mixed, lean is set from its transfer recipients (members' committees and R/D-lean committees, at least 0.67 share; listed in pac/jfc_lean_from_transfers.csv, {'D': 187, 'R': 287})
- Member-run JFCs are often not linked to the member in ccl, so they are classed as JFCs and reach members only through the transfer data.
- Registrant LD-203s include large non-contribution items such as media buys and event sponsorships. They are capped at $7K per item, and payees that are unresolved or candidate committees are not used for the indirect layer.
- Officer matches are by name plus registrant-word corroboration. Common names may still collide, and unmatched names are kept in the ambiguous file.
- names_all.py now rejects surname-only matches inside organisation names (for example "Georgia Safe and Strong" ≠ Rep. Dale Strong). ld203_edges_all.py and build_money_all.py were re-run, so direct-only totals moved slightly: pairs scored $139.34M (R $84.09M / D $55.00M).
- Charts (new files): ranking_money_all_with_pac_top25.png, member_totals_with_pac_top25.png, top_pacs_lobbyist_money_top25.png, network_pac_layer_top40.png.
- Scripts: pac/fec_pac_pass.py → pac/fec_pac_match.py → pac/pas2_and_classify.py → pac/ld203_pac.py → pac/committee_details.py → pac/jfc_transfers.py → pac/build_pac_layer.py → pac/plots_pac.py. Raw OpenFEC caches: pac/committee_detail_raw.jsonl, committee_list_raw.jsonl and jfc_transfers_raw.jsonl. The API key is redacted in pac/api_calls.log.
