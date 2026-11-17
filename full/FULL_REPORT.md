# GOP lobbyist graph: full build report (money + X, top 300)
Generated 2026-11-17, about 1:25 PM EST; bundling layer and money v2 added about 2:10 PM EST. All files are in /workspace/gop-lobby-graph/full/. Checkpoint state is in progress.json.

## Scores (weights)
- **Money score v2** (2026-11-17) = 0.315 × pct(attributable LDA income 2023–26) + 0.315 × pct($ to current GOP members) + 0.18 × pct(number of members funded) + 0.09 × pct(former-employer ties) + **0.10 × pct(FEC Form 3L bundled $ to GOP members' principal/authorized committees and leadership PACs)**.
  - Because no in-scope Form 3L bundling matched any of the 300 (see "Bundling layer"), the bundling term is constant for everyone; it is dropped and the rest divided by 0.9, which is numerically identical to the v1 weights (0.35/0.35/0.20/0.10). The term switches on automatically (rank_money.py) if a matched in-scope bundling row appears. Low-confidence (name-only) bundler matches would not be scored.
  - Dollars are LD-203 self contributions plus FEC individual contributions to members' principal, authorized, JFC and leadership committees linked in FEC bulk candidate-committee linkages, 2023–26.
  - **Fix in v2:** FEC rows to *party* committees (FEC committee type X/Y/Z) are now excluded. The FEC bulk linkage file (ccl) links the NRSC (C00027466) to Dan Sullivan's candidate ID and the Republican Party of Texas to John Cornyn's, so v1 credited NRSC donations to Sullivan. 917 FEC rows ($2.57M as reported) were dropped; Sullivan's scored total fell from $2.00M (118 lobbyists) to $154K (59).
  - LD-203 items that duplicate an FEC record (same member and amount, date within ±3 days) are dropped in favour of the FEC record.
  - Every item is capped at $7,000, so joint-fundraising-committee and party checks are not credited in full to one member.
  - Party-committee payees count at 0.5. PAC-sourced LD-203 items count at 0.5. FEC memo rows and low-confidence name matches are excluded.
- **X score** = 100 × (0.5 × weighted degree/max + 0.3 × distinct members/max + 0.2 × member-authored posts/max). Only in-era edges count, one per thread per pair. Posts made before the person was a member count at half weight.
  - Edge weights: photo_together 3, photo_mention_unclear 1.5, shoutout 1, mention 0.5, list 0.25.
- **Combined** = 0.7 × money + 0.3 × X.

## Top 25 by money score (v2, 2026-11-17 2:10 PM EST)
|#|Lobbyist|Firm|Attrib. income|$ to GOP members|Members funded|Former employer|Form 3L bundled to members|Prev #|Evidence|
|-|-|-|-|-|-|-|-|-|-|
|1|Sam Olswanger|Akin Gump Strauss Hauer & Feld|$10.3M|$294,850|63|Daniel Webster, Marsha Blackburn|$0|1|[LD-203](https://lda.gov/filings/public/contribution/e9d830eb-7988-4f03-ab98-d890ece75650/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202504159755384188)|
|2|Jeffrey Miller|Miller Strategies, Llc|$47.1M|$565,400|97|-|$0|2|[LD-203](https://lda.gov/filings/public/contribution/13a847e8-2ae5-4a95-9bbf-fe619cc5b411/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604279866709363)|
|3|Darren Willcox|W Strategies, Llc|$13.8M|$280,400|78|-|$0|3|[LD-203](https://lda.gov/filings/public/contribution/e2a2e264-354e-44c6-830d-275b32dec5e1/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202304159580769380)|
|4|Jeffery Green|J.A. Green And Company|$12.2M|$315,655|56|-|$0|4|[LD-203](https://lda.gov/filings/public/contribution/17978ddc-7e9a-4b39-887c-3d39513b3c45/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159857784804)|
|5|Paul Edattel|Todd Strategy Group|$8.3M|$380,350|94|-|$0|5|[LD-203](https://lda.gov/filings/public/contribution/efaf969d-9394-42bb-ba48-11ebb1e7f10f/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159857741387)|
|6|Mathew Lapinski|Crossroads Strategies, Llc|$14.3M|$159,626|66|-|$0|7|[LD-203](https://lda.gov/filings/public/contribution/1d4d697b-2dd5-4ea9-86e8-f3290cd25fd0/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202506259762542424)|
|7|Susan Hirschmann|Williams And Jensen, Pllc|$8.6M|$258,423|96|-|$0|6|[LD-203](https://lda.gov/filings/public/contribution/0b78c0e3-61ad-419d-8fc7-218417916267/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202310159597935996)|
|8|Bryan Cunningham|Polaris Government Relations, Ll|$12.4M|$208,099|49|-|$0|9|[LD-203](https://lda.gov/filings/public/contribution/496bb528-24e0-4261-b6cd-13167fd3c0b1/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202401319601235621)|
|9|John Scofield|S-3 Group|$7.6M|$454,000|83|-|$0|10|[LD-203](https://lda.gov/filings/public/contribution/65710127-56fc-4a75-9aed-5cee4ed48418/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202304159580769364)|
|10|Monica Popp|Marshall & Popp, Llc|$7.8M|$185,274|49|John Cornyn|$0|8|[LD-203](https://lda.gov/filings/public/contribution/4f4de75e-0c52-4699-87cd-038db07a97fe/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202304159580769411)|
|11|Robert Wood|Bgr Government Affairs|$9.0M|$176,290|68|-|$0|12|[LD-203](https://lda.gov/filings/public/contribution/b9529fa7-58f0-447f-9bad-7c2c7cee8fc7/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202606119870608206)|
|12|John Mcmanus|The Mcmanus Group|$9.0M|$212,625|61|-|$0|13|[LD-203](https://lda.gov/filings/public/contribution/7a60069f-3311-43a4-b8ca-1a7016b485d4/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202407159653745448)|
|13|Anthony Lazarski|Cornerstone Government Affairs, |$8.2M|$214,650|70|-|$0|14|[LD-203](https://lda.gov/filings/public/contribution/eed4a715-a4ed-46b9-934c-442039118c23/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159857741380)|
|14|Carl Kime|Innovative Federal Strategies, L|$8.0M|$232,850|62|-|$0|15|[LD-203](https://lda.gov/filings/public/contribution/ccb6b688-9a80-42b4-8a5a-d2d5bb8077de/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202406069648874779)|
|15|Letitia White|Innovative Federal Strategies, L|$7.9M|$309,850|53|-|$0|16|[LD-203](https://lda.gov/filings/public/contribution/398f5904-4031-4dbc-b90d-ef28854d4e04/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202504159755527883)|
|16|Erskine Wells|Bgr Government Affairs|$7.6M|$142,000|56|Roger F. Wicker|$0|11|[LD-203](https://lda.gov/filings/public/contribution/fc594e34-094d-4207-bfd2-bc8f6ab9ad53/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159862436438)|
|17|Jessica Tocco|A10 Associates, Llc|$11.6M|$278,041|31|-|$0|17|[LD-203](https://lda.gov/filings/public/contribution/e0b42ef3-b033-4b28-974e-3833ef77088e/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604099857047499)|
|18|James Richards|Cornerstone Government Affairs, |$6.5M|$415,842|109|-|$0|20|[LD-203](https://lda.gov/filings/public/contribution/caf64e81-5713-4711-ab62-550fc1115b37/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159857741389)|
|19|Steven Pfrang|Bgr Government Affairs|$8.3M|$104,625|54|Darin LaHood|$0|19|[LD-203](https://lda.gov/filings/public/contribution/1f67a7dc-db4c-4722-a8fb-70bfab2047c4/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202607019874293291)|
|20|Manny Rossman|Harbinger Strategies, Llc|$8.3M|$148,450|54|-|$0|23|[LD-203](https://lda.gov/filings/public/contribution/4d829120-d384-4c3a-9d21-684c680393b8/print/)|
|21|Bill Viney|Bgr Government Affairs|$11.3M|$123,462|48|-|$0|24|[LD-203](https://lda.gov/filings/public/contribution/06390cdc-f61d-4531-9c19-0762afe0d5a1/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202607019874293313)|
|22|Kyle Nevins|Harbinger Strategies, Llc|$8.4M|$142,450|52|-|$0|25|[LD-203](https://lda.gov/filings/public/contribution/88769eac-09c4-433b-858d-3b90e34eda64/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202404159627911458)|
|23|Randall Russell|The Russell Group, Inc.|$7.7M|$215,100|47|-|$0|22|[LD-203](https://lda.gov/filings/public/contribution/e3682ea2-d02f-4421-b037-b224d46fd84e/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202507159763468031)|
|24|Zachary Rudisill|Akin Gump Strauss Hauer & Feld|$13.9M|$112,203|42|-|$0|18|[LD-203](https://lda.gov/filings/public/contribution/d7127935-d0b2-4e8c-99ed-6e5569b146e2/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159857742923)|
|25|Marc Lampkin|Brownstein Hyatt Farber Schreck,|$7.9M|$133,250|54|-|$0|26|[LD-203](https://lda.gov/filings/public/contribution/86b19d18-8b30-4de2-b12c-16a400a8c9db/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202310139597608830)|

Previous version: ranking_money.prev_20261117_1407.csv. Changes come from the FEC party-committee fix, not from bundling (see "Bundling layer").

## X-based ranking
After all 300 names were run (the top 88 earlier, the remaining 212 on 2026-11-17), **6 lobbyists have in-era X edges and 294 of 300 tie at zero.** A meaningful X top 25 cannot be produced. The six:

|X rank|Lobbyist|Firm|Weighted degree|Members|Posts|Evidence|
|-|-|-|-|-|-|-|
|1|Carlos Trujillo|Continental Strategy|2.75|2|2|Patronis (pre-member): [photo, 'my friend Ambassador'](https://x.com/JimmyPatronis/status/1761180836555063678), [praise of Continental hire](https://x.com/JimmyPatronis/status/1857366982032507226); own post tagging @RepCarlos ([link](https://x.com/AmbCTrujillo/status/1872018993365807251))|
|2|Timothy Costa|Continental Strategy|2.0|1 (Meuser)|2|[RepMeuser: CoS 'moving on from Capitol Hill today… trusted political advisor'](https://x.com/RepMeuser/status/1898115442012831843); [Meuser4Congress: 'will oversee campaign operations and fundraising'](https://x.com/Meuser4Congress/status/1898121009393189167) (2025-03-07)|
|3|Norm Coleman|Hogan Lovells|1.5|2 (Emmer, Moreno)|2|[Emmer: 'Excellent introduction of @PeteHegseth from … Norm Coleman'](https://x.com/GOPMajorityWhip/status/1879187323599917182); [Moreno (pre-member, half weight): 'Proud to be endorsed by … Sen. Norm Coleman'](https://x.com/berniemoreno/status/1683489624541233155)|
|4|William Wichterman|Covington & Burling|1.5|1 (Cramer)|1|[Cramer: 'Great to talk with Susan Gates and Bill Wichterman about the upcoming @FaithandLaw Evening Forum' + photo](https://x.com/SenKevinCramer/status/1923094567600943513) (the caption doesn't say who is in the photo, so it is classed photo_mention_unclear)|
|5|Kate Hull|Fierce Government Relations|1.0|1 (Tim Scott)|1|[Tim Scott: 'Wastewater Action Alliance Executive Director Kate Hull highlights…' (video)](https://x.com/SenatorTimScott/status/2066506450420019655); WAA is a Fierce LDA client|
|6|John Leganski|Harbinger Strategies|0.25|1 (Stefanik)|1|[Stefanik book list: 'GLORY, GRIEF, & THE GAVEL by John Leganski'](https://x.com/EliseStefanik/status/2047304247738253502) (list mention)|

**Out of era or rejected:**
- Chris LaCivita's 8 member posts are all from 2024, before his first LDA quarter (2025Q1), so they score 0 (for example, [Ernst photo_together](https://x.com/joniernst/status/1813333703411823065)).
- A 2025-01-21 Meuser post thanking "my Chief of Staff Tim Costa" was rejected because Costa was still Hill staff then; he left on 2025-03-07.
- Greg Walden's only hit is a historical list (not_relationship, weight 0). A scoring bug was still counting it toward members and posts. It is fixed, and Walden's X score went from 25 to 0.
- 13 other hits from the 212-name run were rejected: namesakes (a sheriff, a deputy, a fire chief, a judge, CEOs), the Bryce Harlow Award/Foundation, a historical reference, and an edit-history duplicate. See x/x_hits_rejected.csv.

## Top 25 combined
1. Carlos Trujillo (71.57) | 2. Sam Olswanger (66.36) | 3. Jeffrey Miller (65.54) | 4. Darren Willcox (63.51) | 5. Jeffery Green (63.05) | 6. Paul Edattel (61.94) | 7. Mathew Lapinski (61.62) | 8. Susan Hirschmann (61.33) | 9. Bryan Cunningham (60.55) | 10. John Scofield (60.54) | 11. Monica Popp (60.21) | 12. Robert Wood (60.06) | 13. John Mcmanus (60.0) | 14. Anthony Lazarski (59.64) | 15. Carl Kime (59.42) | 16. Letitia White (59.41) | 17. Erskine Wells (59.11) | 18. Jessica Tocco (58.47) | 19. James Richards (58.16) | 20. Steven Pfrang (57.68) | 21. Manny Rossman (57.2) | 22. Bill Viney (57.1) | 23. Kyle Nevins (56.92) | 24. Randall Russell (56.76) | 25. Timothy Costa (56.63)

**Caveat:** X is 30% of the combined score but rests on 9 scored posts for 6 people. Trujillo's #1 comes from three posts. Tim Costa jumps from #147 to #25 on two Meuser posts; he is Meuser's former chief of staff and already has a former-employer money tie. The money ranking remains the more reliable measure.

## Coverage
- **LDA:** 16 quarters of LD-2 reports and 7 LD-203 periods, crawled in full.
- **Money layer, LD-203:** 15,969 items to current GOP members from 291 of the 300. 7,779 of them duplicate FEC rows.
- **Money layer, FEC:** 11,891 matched individual rows (10,717 high confidence: employer matches the registrant) for 262 people; 917 rows to party committees excluded in v2. These came from FEC bulk files (indiv24/indiv26), not the API, so there were no DEMO_KEY gaps to re-run.
- **Money layer, pairs (v2):** 8,357 lobbyist–member pairs covering 266 of 274 GOP members.
  - $23.0M scored (v1: $24.9M; the difference is the excluded party-committee rows).
  - Former-employer ties: 155 (62 lobbyists, 47 members).
  - Jurisdiction overlap: recorded as a pair attribute, weight 0.
- **X layer:**
  - Name queries covered the top 88 (union of the top 70 by money and top 40 by income). 9 were excluded as ambiguous common or legislator names; Jeff Miller of Miller Strategies is one of them.
  - For those 79 people, queries ran against 405 member handles: official, alternate/personal and leadership accounts.
  - @handle queries were also run for Ballard, Trujillo, Lanza, Walden and LaCivita.
  - **Top-88 pass:** 79 searches.
  - **Remaining 212 names:** 177 searches, all done (status in x/pending_queries_rest_status.json; call log in x/rest_run/calls_rest.csv).
    - 165 were the queued queries.
    - 12 were supplemental queries (S*_*) for member chunk 13, which the original queue had dropped (26-34 handles per block, e.g. RepDaveTaylor, RepFedorchak).
    - 2 more lookups read the full text of truncated posts.
  - **Rest-run hits:** 20 raw posts, giving 7 kept edges and 13 rejects (one reject is an edit-history duplicate of a kept post).
  - **Query shape:** name-only (quoted full name plus nickname variants), from: member handles, -is:retweet, since 2022-11-17. @handle mentions of the 212 names were not searched because their X handles are unknown.
  - **Budget:** 575 of 1,000 X reads left today at 1:48 PM EST; the limit resets at 7 PM EST. Another consumer shares this quota.

## Bundling layer (FEC Form 3L), added 2026-11-17
**Result: $0 of Form 3L bundling to GOP members' committees matched any of the 300 lobbyists.** The reason is on the filing side: in the 2024 and 2026 cycles, only one current GOP member's committee filed a Form 3L at all.

- **Method.** OpenFEC /filings/?form_type=F3L for cycles 2024 and 2026 (608 filings from 142 committees; 596 most-recent versions). Cross-checked with /efile/filings/ (F3LN/F3LA, 113 filings since 2026-07-15, all already in the set). Itemized bundler lines (SA3L records) were parsed from each filing's .fec file on docquery.fec.gov (1,446 lines). Schedule A does not carry 3L items (checked: 0 rows for an F3L image number and for a known bundler name), and Schedule A conduit fields are earmark conduits such as WinRed, not lobbyist bundling, so they were not used.
- **GOP member committees.** 649 committees: principal/authorized from FEC bulk ccl24/ccl26 for every current Republican's FEC candidate IDs, plus 280 leadership PACs from OpenFEC sponsor_candidate_id (bundling/gop_member_committees.csv). A direct all-time query of all 649 for F3L returned 54 filings ever; only 2 fall in 2023–26.
- **The only in-scope filings:** Messmer for Congress (Rep. Mark Messmer, IN-08), 12P and Q2 2024 reports: AIPAC PAC (C00797670), a lobbyist/registrant PAC, bundled $297,943.33 ([12P PDF](https://docquery.fec.gov/pdf/422/202404259636745422/202404259636745422.pdf), [Q2 PDF](https://docquery.fec.gov/pdf/837/202407159660900837/202407159660900837.pdf)). AIPAC is not one of the 300. That row is in edges_money_bundling.csv.
- **Matching rules.** Individual bundlers: last name plus first name or nickname against the 300, confidence high when the reported employer matches the registrant firm, medium for name plus DC/VA/MD address, low for name only. Org/PAC bundlers: exact normalized firm name against the 300's registrants.
- **Amounts.** Most-recent filing versions only. Per committee, bundler and half-year, total = max(semi-annual cumulative, sum of period amounts), so semi-annual running totals are not double-counted.
- **Context, not scored (Trump committees; Trump is not a member of Congress).** Five of the 300 appear as bundlers, all with employer matching their firm (bundling/bundling_top300_to_nonmember_committees.csv):
  - Geoff Verhoff (Akin Gump): $5.48M to Trump 47 Committee (2024).
  - Jeffrey Miller (Miller Strategies, Austin TX): $3.62M: $2.69M Trump 47 Committee, $852.7K Trump Save America JFC, $84.0K Never Surrender (Trump leadership PAC).
  - Brian Ballard (Ballard Partners): $1.81M: $1.76M Trump 47 Committee, $50.7K Trump Save America JFC.
  - Oswaldo Palomo (Chartwell Strategy Group): $243.5K to Trump 47 Committee.
  - Marc Lampkin (Brownstein Hyatt): $44.9K to Trump 47 Committee.
  - Total $11,205,462.63.
- **Caveats.** Form 3L is filed only when a committee receives bundled contributions over the threshold ($23,300 in 2024) from a registered lobbyist, registrant or their PAC, and the committee itself decides what counts as "bundled". So the near-absence of GOP filings means none were reported, not that no bundling happened. Paper-era filings before 2024 by Senate committees were covered only to the extent FEC indexed them as F3L. Leadership PACs were found through the sponsor field; any leadership PAC without a sponsor ID in OpenFEC would be missed.
- **API use:** about 45 OpenFEC calls (limit 60 per window, backoff in bundling/fecapi.py); the key is read from file and redacted in bundling/api_calls.log.

## Gaps and caveats
- **X data is extremely sparse.** GOP members almost never name or tag the highest-earning lobbyists, which is consistent with the pilot. No face recognition was used: people are identified only from captions and @mentions.
- **Bundling (Form 3L) covered 2026-11-17** with a real OpenFEC key: no in-scope matches (see above).
- **Leadership PACs** are captured through LD-203 payee and honoree names only. FEC matching covers principal and authorized committees only.
- **FEC name pool** used LDA first names only, so donors filing under a nickname may be missed.
- **Income attribution** (equal split per filing) and **ID merging** are heuristics. Amended LD-2 reports were not reconciled.
- **Honoree matching** is name-based ('first+last', or a unique surname with context checks). Spot-check the unique_last rows.
- Folder compacted to about 104M: LDA files gzipped, FEC zips deleted.

## Files
- Selection: selected_top300.csv, people_universe_scored.csv, SELECTION_RULES.md
- Bundling: edges_money_bundling.csv (in-scope rows, PDF and .fec links), bundling/ (raw F3L filing index, parsed SA3L lines f3l_sa3l_all_2024_2026.csv, GOP member committee map, Trump-committee context file, scripts)
- Money edges: edges_money_ld203.csv (filing_uuid and URL), edges_money_fec_raw.csv (fec_sub_id and image URL), edges_money_former_employer.csv, edges_money_pairs.csv
- X: x/x_edges_handreviewed.csv, x/x_hits_rejected.csv, x/x_calls_full.csv
- Rankings: ranking_money.csv, ranking_x.csv, ranking_combined.csv
- Charts: network_top50.png, ranking_money_top25.png
- Previous versions: *.prev_20261117_1407.* (before bundling layer and party-committee fix)