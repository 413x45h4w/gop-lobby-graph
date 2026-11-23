# Ethics layer (built 2026-11-22T21:13:50-05:00)

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
- `house_annual_holdings.csv` House annual FD (filing type O, filing years 2024 and 2025 = calendar 2023 and 2024) Schedule A assets parsed from electronic PDFs
  (asset text, ticker, asset code, value range). Wrapped asset names are sometimes truncated to the ticker line, e.g. "(HQH)". Paper/scanned annual reports are not parsed.
- `house_annual_gifts_travel.csv` Schedule G gifts and Schedule H travel reimbursements from the same PDFs (raw text kept; parsing is approximate).
- `edges_member_company_holdings.csv` member -> LD-2 org (company that lobbies) from House Schedule A + Senate Part 3, summed value-range bounds.
- Gaps: House 2026 annual filings are not yet indexed as type O in the Clerk's 2026 index; House gift reports exist only inside FD PDFs (Schedule G above).
  Senate privately funded travel (Rule 35 pre-approval forms) is not in eFD as structured data; only annual-report travel reimbursements are included.

Stats
```
{
 "house_tx": 16165,
 "house_tx_bioguide": 16150,
 "house_tx_org": 3631,
 "senate_tx": 3986,
 "senate_tx_bioguide": 3986,
 "senate_tx_org": 970,
 "house_travel": 7206,
 "house_travel_bioguide": 7193,
 "house_travel_org": 775,
 "house_fd_assets": 31981,
 "house_fd_assets_org": 3908,
 "house_fd_H": 346,
 "house_fd_G": 18,
 "house_annual_holdings_rows": 31981,
 "house_annual_gift_travel_rows": 364,
 "member_company_holding_edges": 2136,
 "stock_tx_rows": 20151,
 "member_company_edges": 8814,
 "senate_holdings": 36916,
 "senate_gifts": 36,
 "senate_travel": 100,
 "travel_sponsor_edges": 4427,
 "built_at": "2026-11-22T20:58:50-05:00"
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
| `edges_member_company_holdings.csv` | 2,136 |
| `edges_member_company_trades.csv` | 8,814 |
| `edges_travel_sponsor_to_member.csv` | 5,116 |
| `house_annual_gifts_travel.csv` | 364 |
| `house_annual_holdings.csv` | 31,981 |
| `house_privately_funded_travel.csv` | 7,941 |
| `senate_annual_gifts.csv` | 36 |
| `senate_annual_holdings.csv` | 36,916 |
| `senate_annual_travel_reimbursements.csv` | 100 |
| `stock_transactions.csv` | 20,151 |
| `raw/house_fd_annual_docs.jsonl` | 804 |
| `raw/house_fd_annual_items.jsonl` | 32,858 |
| `raw/house_ptr_docs.jsonl` | 1,903 |
| `raw/house_ptr_transactions.jsonl` | 16,165 |
| `raw/senate_efd_reports.jsonl` | 987 |

## Build log (append-only)
- 2026-11-22T20:30:02-05:00: rebuilt; counts above.
- 2026-11-22T20:30:12-05:00: rebuilt; counts above.
- 2026-11-22T20:35:36-05:00: rebuilt; counts above.
- 2026-11-22T21:13:40-05:00: rebuilt; counts above.
- 2026-11-22T21:13:50-05:00: rebuilt; counts above.
