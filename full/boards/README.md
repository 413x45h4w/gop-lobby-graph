# boards/: corporate boards of top lobbying clients (SEC)

Built 2026-11-22 ET by `scripts/build_boards.py`. Append-only (rebuilds keep `*.prev_<YYYYMMDD_HHMM>.*`).

## Method
1. **Top clients:** `lda_clients_spend_2023_26.csv` (23,895 clients) aggregates LDA client spend for 2023-2026 from the local LD-2 crawl (`lda/ld2_universe`, 297,217 filings).
   - Spend is outside-registrant income plus in-house expenses, grouped by normalized client name (`scripts/orgnorm.py`).
   - `full/ld2/` did not exist at build time.
   - The known outlier client "State of Loc Nation…" (see `money_all/income_outliers_excluded.csv`) is skipped.
2. **Company match:** each of the top 500 clients is matched to an SEC CIK via `company_tickers.json` (listed companies only). The matching is tried in this order:
   - exact normalized name (183)
   - the name minus generic LDA suffixes such as SERVICES, AFFILIATES or VARIOUS SUBSIDIARIES (14, e.g. Amazon.com Services→Amazon.com Inc)
   - one manual parent alias: Google Client Services→Alphabet
   - That gives **198 public companies**. The other clients in the top 500 are associations, unions, private firms or foreign parents.
3. **Directors:** reporting owners with relationship "Director" on Forms 3/4/5 for the issuer, from the SEC Insider Transactions Data Sets for 2025Q1-2026Q1 (`raw/*_form345.zip`). The latest filing date and accession are kept.
4. **Proxy check:** the latest **DEF 14A** per CIK (data.sec.gov submissions API, fetched 2026-11-22). Only a token set is cached in raw/ (not committed).
   - `high_form345_and_proxy`: the director's surname and first name both appear in the proxy text.
   - `medium_form345_only`: the proxy exists but the name was not found. Usually a director who joined or left after the proxy.
   - `medium_form345_no_proxy_text`: no DEF 14A found (18 companies, mostly foreign filers that file 20-F).

## Files
| file | rows | what |
|---|---|---|
| `companies_top_lda_clients_sec.csv` | 198 | client→CIK map, ticker, LDA rank and spend, DEF 14A url and date, n directors |
| `edges_person_company_board.csv` | 2,212 | **person→company board edges**: 1,999 high, 213 medium. Lobbyist and member match columns. |
| `board_interlocks_top_clients.csv` | 216 | directors who sit on 2 or more top-client boards (same SEC owner CIK) |
| `board_person_match_ambiguous.csv` | 81 | name hits not accepted |
| `lda_clients_spend_2023_26.csv` | 23,895 | full client spend table (also used by outside_money/ and nonprofits/) |
| `boards_stats.json` | | run statistics |

Keys:
- People: `director_sec_cik` (stable SEC person id)
- Members: `bioguide`
- Lobbyists: `person_id` (see `nonprofits/README.md`; same matcher, `nonprofits/scripts/personmatch.py`)
- Clients: `client_key`

## Matches
- **Former members on top-client boards (6, `medium_name_former_member`, all checked by hand as plausible):**
  - Leon Panetta (Oracle)
  - Bob Kerrey (Tenet Healthcare)
  - Roy Blunt (Tenet Healthcare)
  - Rob Portman (Procter & Gamble)
  - Evan Bayh (Marathon Petroleum)
  - John E. Sununu (Boston Scientific)
- **Lobbyists:** 0 accepted. Name-only hits (e.g. "John Cahill" at American Airlines, "David Weinberg" at Coca-Cola) were moved to the ambiguous file, because corporate directors are mostly executives with namesakes in the 21k lobbyist universe. Only org-linked matches count, and none occurred.
- **Interlocks:** examples include Patricia Russo (GM, HPE, Merck), Wesley Bush (Cisco, GE, GM), Brad Smith (Amazon, Humana, JPMorgan), Robin Washington (Alphabet, Honeywell, Salesforce) and Scott Gottlieb (Illumina, Pfizer, UnitedHealth).

## Gaps
- **Former executive-branch officials** on boards are not identified. No structured public roster of former officials was available; DEF 14A biographies would need text parsing.
- Private companies, foreign parents (most file 20-F) and trade associations have no SEC director data. Association boards are in `nonprofits/edges_person_org_officer.csv` instead.
- Directors who filed no Form 3/4/5 in 2025Q1-2026Q1 are missed. Rare for sitting directors, who get annual equity grants.
- Subsidiary→parent mapping beyond the suffix rule and the one alias is not done, so some top clients (e.g. BCBS plans, private Koch Industries) have no board data.

## Run log (append-only)
- 2026-11-22 20:27-20:38 ET: first build. Second run demoted name-only lobbyist matches; third run used the tightened congressional-context regex.
