# GOP lobbyist graph: full build report (money + X, top 300)
Generated 2026-11-17, about 1:25 PM EST. All files are in /workspace/gop-lobby-graph/full/. Checkpoint state is in progress.json.

## Scores (weights)
- **Money score** = 0.35 × percentile(attributable LDA income 2023–26) + 0.35 × percentile($ to current GOP members) + 0.20 × percentile(number of members funded) + 0.10 × percentile(former-employer ties).
  - Dollars are LD-203 self contributions plus FEC individual contributions to members' principal and authorized committees, 2023–26.
  - LD-203 items that duplicate an FEC record (same member and amount, date within ±3 days) are dropped in favour of the FEC record.
  - Every item is capped at $7,000, so joint-fundraising-committee and party checks are not credited in full to one member.
  - Party-committee payees count at 0.5. PAC-sourced LD-203 items count at 0.5. FEC memo rows and low-confidence name matches are excluded.
- **X score** = 100 × (0.5 × weighted degree/max + 0.3 × distinct members/max + 0.2 × member-authored posts/max). Only in-era edges count, one per thread per pair. Posts made before the person was a member count at half weight.
  - Edge weights: photo_together 3, photo_mention_unclear 1.5, shoutout 1, mention 0.5, list 0.25.
- **Combined** = 0.7 × money + 0.3 × X.

## Top 25 by money score
|#|Lobbyist|Firm|Attrib. income|$ to GOP members|Members funded|Former employer|Evidence|
|-|-|-|-|-|-|-|-|
|1|Sam Olswanger|Akin Gump Strauss Hauer & Feld|$10.3M|$305,475|64|Daniel Webster|Marsha Blackburn|[LD-203](https://lda.gov/filings/public/contribution/e9d830eb-7988-4f03-ab98-d890ece75650/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202504159755384188)|
|2|Jeffrey Miller|Miller Strategies, Llc|$47.1M|$613,100|98|-|[LD-203](https://lda.gov/filings/public/contribution/13a847e8-2ae5-4a95-9bbf-fe619cc5b411/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202310209598683503)|
|3|Darren Willcox|W Strategies, Llc|$13.8M|$280,400|78|-|[LD-203](https://lda.gov/filings/public/contribution/e2a2e264-354e-44c6-830d-275b32dec5e1/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202304159580769380)|
|4|Jeffery Green|J.A. Green And Company|$12.2M|$315,655|56|-|[LD-203](https://lda.gov/filings/public/contribution/17978ddc-7e9a-4b39-887c-3d39513b3c45/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202605079866866735)|
|5|Paul Edattel|Todd Strategy Group|$8.3M|$380,350|94|-|[LD-203](https://lda.gov/filings/public/contribution/efaf969d-9394-42bb-ba48-11ebb1e7f10f/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159857741387)|
|6|Susan Hirschmann|Williams And Jensen, Pllc|$8.6M|$272,423|97|-|[LD-203](https://lda.gov/filings/public/contribution/0b78c0e3-61ad-419d-8fc7-218417916267/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202310159597935996)|
|7|Mathew Lapinski|Crossroads Strategies, Llc|$14.3M|$159,626|66|-|[LD-203](https://lda.gov/filings/public/contribution/1d4d697b-2dd5-4ea9-86e8-f3290cd25fd0/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202506259762542424)|
|8|Monica Popp|Marshall & Popp, Llc|$7.8M|$236,524|49|John Cornyn|[LD-203](https://lda.gov/filings/public/contribution/4f4de75e-0c52-4699-87cd-038db07a97fe/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202304159580769411)|
|9|Bryan Cunningham|Polaris Government Relations, Ll|$12.4M|$228,724|49|-|[LD-203](https://lda.gov/filings/public/contribution/496bb528-24e0-4261-b6cd-13167fd3c0b1/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202401319601235621)|
|10|John Scofield|S-3 Group|$7.6M|$454,000|83|-|[LD-203](https://lda.gov/filings/public/contribution/65710127-56fc-4a75-9aed-5cee4ed48418/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202304159580769364)|
|11|Erskine Wells|Bgr Government Affairs|$7.6M|$201,000|56|Roger F. Wicker|[LD-203](https://lda.gov/filings/public/contribution/fc594e34-094d-4207-bfd2-bc8f6ab9ad53/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202608209899729676)|
|12|Robert Wood|Bgr Government Affairs|$9.0M|$176,290|68|-|[LD-203](https://lda.gov/filings/public/contribution/b9529fa7-58f0-447f-9bad-7c2c7cee8fc7/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202606119870608206)|
|13|John Mcmanus|The Mcmanus Group|$9.0M|$212,625|61|-|[LD-203](https://lda.gov/filings/public/contribution/7a60069f-3311-43a4-b8ca-1a7016b485d4/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202407159653745448)|
|14|Anthony Lazarski|Cornerstone Government Affairs, |$8.2M|$227,150|70|-|[LD-203](https://lda.gov/filings/public/contribution/eed4a715-a4ed-46b9-934c-442039118c23/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159857741380)|
|15|Carl Kime|Innovative Federal Strategies, L|$8.0M|$250,350|63|-|[LD-203](https://lda.gov/filings/public/contribution/ccb6b688-9a80-42b4-8a5a-d2d5bb8077de/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202303209579424830)|
|16|Letitia White|Innovative Federal Strategies, L|$7.9M|$309,850|53|-|[LD-203](https://lda.gov/filings/public/contribution/398f5904-4031-4dbc-b90d-ef28854d4e04/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202504159755527883)|
|17|Jessica Tocco|A10 Associates, Llc|$11.6M|$299,041|32|-|[LD-203](https://lda.gov/filings/public/contribution/e0b42ef3-b033-4b28-974e-3833ef77088e/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604209863288937)|
|18|Zachary Rudisill|Akin Gump Strauss Hauer & Feld|$13.9M|$155,953|43|-|[LD-203](https://lda.gov/filings/public/contribution/d7127935-d0b2-4e8c-99ed-6e5569b146e2/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159857742923)|
|19|Steven Pfrang|Bgr Government Affairs|$8.3M|$120,471|55|Darin LaHood|[LD-203](https://lda.gov/filings/public/contribution/1f67a7dc-db4c-4722-a8fb-70bfab2047c4/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202607019874293291)|
|20|James Richards|Cornerstone Government Affairs, |$6.5M|$429,842|109|-|[LD-203](https://lda.gov/filings/public/contribution/caf64e81-5713-4711-ab62-550fc1115b37/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202605209870085084)|
|21|Hazen Marshall|Marshall & Popp, Llc|$7.9M|$148,900|38|Mitch McConnell|[LD-203](https://lda.gov/filings/public/contribution/568d2434-e5d8-42f0-a8e8-46414a943609/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202604159857803173)|
|22|Randall Russell|The Russell Group, Inc.|$7.7M|$215,100|47|-|[LD-203](https://lda.gov/filings/public/contribution/e3682ea2-d02f-4421-b037-b224d46fd84e/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202507159763468031)|
|23|Manny Rossman|Harbinger Strategies, Llc|$8.3M|$148,450|54|-|[LD-203](https://lda.gov/filings/public/contribution/4d829120-d384-4c3a-9d21-684c680393b8/print/)|
|24|Bill Viney|Bgr Government Affairs|$11.3M|$123,462|48|-|[LD-203](https://lda.gov/filings/public/contribution/06390cdc-f61d-4531-9c19-0762afe0d5a1/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202607019874293313)|
|25|Kyle Nevins|Harbinger Strategies, Llc|$8.4M|$142,450|52|-|[LD-203](https://lda.gov/filings/public/contribution/88769eac-09c4-433b-858d-3b90e34eda64/print/) · [FEC](https://docquery.fec.gov/cgi-bin/fecimg/?202404159627911458)|

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
1. Carlos Trujillo (71.32) | 2. Sam Olswanger (66.37) | 3. Jeffrey Miller (65.54) | 4. Darren Willcox (63.43) | 5. Jeffery Green (62.88) | 6. Paul Edattel (61.86) | 7. Susan Hirschmann (61.33) | 8. Mathew Lapinski (61.3) | 9. Monica Popp (61.09) | 10. Bryan Cunningham (60.85) | 11. John Scofield (60.54) | 12. Erskine Wells (60.34) | 13. Robert Wood (59.81) | 14. John Mcmanus (59.73) | 15. Anthony Lazarski (59.72) | 16. Carl Kime (59.57) | 17. Letitia White (59.22) | 18. Jessica Tocco (58.82) | 19. Zachary Rudisill (58.44) | 20. Steven Pfrang (58.26) | 21. James Richards (58.16) | 22. Hazen Marshall (57.07) | 23. Timothy Costa (56.63) | 24. Randall Russell (56.38) | 25. Manny Rossman (56.36)

**Caveat:** X is 30% of the combined score but rests on 9 scored posts for 6 people. Trujillo's #1 comes from three posts. Tim Costa jumps from #147 to #23 on two Meuser posts; he is Meuser's former chief of staff and already has a former-employer money tie. The money ranking remains the more reliable measure.

## Coverage
- **LDA:** 16 quarters of LD-2 reports and 7 LD-203 periods, crawled in full.
- **Money layer, LD-203:** 15,969 items to current GOP members from 291 of the 300. 7,779 of them duplicate FEC rows.
- **Money layer, FEC:** 11,891 matched individual rows (10,717 high confidence: employer matches the registrant) for 262 people.
- **Money layer, pairs:** 8,416 lobbyist–member pairs covering 266 of 274 GOP members.
  - $24.9M scored ($26.9M as reported).
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

## Gaps and caveats
- **X data is extremely sparse.** GOP members almost never name or tag the highest-earning lobbyists, which is consistent with the pilot. No face recognition was used: people are identified only from captions and @mentions.
- **Bundling (Form 3L) not covered.** OpenFEC DEMO_KEY rate limits are too low, and a free key requires an email signup, which was not done.
- **Leadership PACs** are captured through LD-203 payee and honoree names only. FEC matching covers principal and authorized committees only.
- **FEC name pool** used LDA first names only, so donors filing under a nickname may be missed.
- **Income attribution** (equal split per filing) and **ID merging** are heuristics. Amended LD-2 reports were not reconciled.
- **Honoree matching** is name-based ('first+last', or a unique surname with context checks). Spot-check the unique_last rows.
- Folder compacted to about 104M: LDA files gzipped, FEC zips deleted.

## Files
- Selection: selected_top300.csv, people_universe_scored.csv, SELECTION_RULES.md
- Money edges: edges_money_ld203.csv (filing_uuid and URL), edges_money_fec_raw.csv (fec_sub_id and image URL), edges_money_former_employer.csv, edges_money_pairs.csv
- X: x/x_edges_handreviewed.csv, x/x_hits_rejected.csv, x/x_calls_full.csv
- Rankings: ranking_money.csv, ranking_x.csv, ranking_combined.csv
- Charts: network_top50.png, ranking_money_top25.png