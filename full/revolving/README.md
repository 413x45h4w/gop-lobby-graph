# Revolving-door layer

Built 2026-11-22 ET by `build_revolving.py`. Shared name matcher: `memberlex.py`. It covers every legislator with a term ending on or after 2009-01-03; the former-member check uses everyone since 1970. It is title-anchored ("Senator X", "Rep. First Last", "Office of ...") and returns *no match* when a surname is ambiguous. Those cases are logged in `covered_position_ambiguous_member.csv`.

**LegiStorm is paywalled and was not used.** The public substitutes are the House Statement of Disbursements and the Report of the Secretary of the Senate.

## Sources (raw pull logs in raw/)
1. **LD-2 `covered_position` text**: 13,206 distinct (lobbyist, text) pairs from the 297,355 LD-2 reports in `../ld2/raw`. Each segment (split on `;`) is parsed into a member office, a committee (thomas_id), an executive agency and/or a self-identified former member.
2. **House Statement of Disbursements**: the 41 quarterly DETAIL CSVs from 2016 Q1 to 2026 Q2 (house.gov, pulled 2026-11-22 20:10 ET; `raw/sod_pull_log.jsonl`). The files were streamed. Only personnel-compensation rows (budget object class 11) were kept, aggregated per office, staffer and title in `raw/sod_personnel_rows.csv.gz` (723k rows). 2019 Q1 is not posted on house.gov's archive and is a gap.
3. **Secretary of the Senate reports**: 30 semiannual reports (60 PDF parts, GovInfo CDOC 112th–119th, Apr 2011 to Mar 2026), streamed through `pdftotext`. Payroll lines (office, `LAST, FIRST`, title, amount) are in `raw/senate_payroll_rows.csv.gz` (192,180 rows). Each report's period comes from its position in senate.gov's newest-first list, checked against the 118sdoc13 header (04/01/2024–09/30/2024).

## Files
| file | rows | what |
|---|---|---|
| edges_former_staffer_member.csv | 17,199 | lobbyist → member (bioguide; `member_current` flag): one row per piece of evidence (covered-position segment or payroll record) |
| former_staffer_member_pairs.csv | 8,858 | deduplicated lobbyist–member pairs with `sources` and `best_confidence`: 5,140 lobbyists, 476 current members |
| edges_former_staffer_committee.csv | 5,832 | lobbyist → committee staff service |
| edges_lobbyist_former_agency.csv | 3,436 | lobbyist → former executive agency (White House, DoD, Treasury and others), from covered positions |
| former_member_lobbyists.csv | 263 | lobbyists who are former members of Congress |
| covered_position_parsed.csv.gz | 25,492 | every covered-position segment with its parse |
| payroll_name_matches_all.csv.gz | 14,368 | every payroll ↔ lobbyist name match, including low-confidence ones |

## Confidence
- **Covered position**: `high` when the text gives first and last name ("Senator Tom Cotton"). `medium` when it gives a title and surname only and that surname is unique among members ("Rep Webster"). `rejected_contact_list` when the text names 3 or more members with no staff-role word (70 rows).
- **Payroll**: `high` when the lobbyist's own covered position names the same member or committee. `medium` when the (last, first) name maps to exactly one person in the lobbyist universe and the payroll period doesn't overlap that person's LD-2 lobbying quarters. `low` when the name is shared by several people or there is a timeline overlap. `low` matches are kept only in payroll_name_matches_all and are never edges. Names are matched with nickname folding (Bob/Robert and the like). There is no middle-name check, so `medium` payroll edges are name matches, not verified identities.
- **Pairs** supported by two sources (covered position + House or Senate payroll) are always `high`: 2,445 pairs.
- **Former members**: `high` (97) = the covered position says Member/Representative/Senator **and** first+last name matches a unique legislator. `self_identified_lastname_match` / `self_identified_name_unmatched` = flagged by text only. `name_only_unverified` (118) = exact first+last match with a former legislator (term ended 1995 or later) but no self-identification. These may be namesakes and should not be scored.

## Gaps
- Most junior staff are not "covered officials", so the LD-2 text undercounts staff history. The payroll match covers House staff from 2016 on and Senate staff from Apr 2011 on only.
- Senate payroll rows carry the report period, not exact employment dates.
- Middle names are not used, so common names stay `low`.
