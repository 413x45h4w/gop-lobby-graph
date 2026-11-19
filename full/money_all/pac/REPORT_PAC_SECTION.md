
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
