# FARA layer (DOJ Foreign Agents Registration Act)

Bulk CSVs from `https://efile.fara.gov/bulk/zip/` (Registrants, ForeignPrincipals, ShortForms, RegistrantDocs), pulled 2026-11-22 20:09 ET (`raw/PULLED_AT.txt`). The zips are kept in `raw/` (5 MB). All 3,064 **Supplemental Statements** date-stamped 2023-01-01 or later were downloaded (`fetch_ss.py`, 20:11–20:16 ET) and text-extracted with `pdftotext -layout`. 3,062 succeeded. The text is kept on the box only (`raw/ss_text/`, git-ignored), and the PDFs were not kept. `supplemental_statements_manifest.csv` lists each document's URL and pull time.

FARA has **no structured contact or contribution data**. Contacts with congressional offices and political contributions exist only inside the statement PDFs, so the contact and contribution edges below are parsed from text.

## Files
| file | rows | what |
|---|---|---|
| fara_registrants.csv | 7,108 | every registrant ever, with `active_2023_plus` and a link to LDA registrant ids by normalized name (181 of 872 active registrants match an LDA registrant) |
| edges_principal_registrant.csv | 17,795 | foreign principal (with country) → registrant, with dates |
| edges_registrant_agent.csv | 44,804 | registrant → short-form agent (individual), matched to lobbyist `person_id` |
| edges_fara_contact_member.csv | 17,641 | registrant → member mention or contact in a supplemental statement (one row per document × member), with an attributed foreign principal |
| edges_principal_registrant_member.csv | 16,191 | the chained edge foreign principal → registrant → member, plus the registrant's LDA-matched agents |
| edges_fara_contribution_member.csv | 19,960 | political contributions reported in supplemental statements (date, donor, recipient, amount), linked to a member where possible, deduplicated across documents |

## Matching and confidence
- **Agent → lobbyist**: `high` = same (last, first) name **and** the person lobbied under an LDA registrant whose name matches the FARA registrant. `medium` = the name maps to exactly one person in the universe. `low_multiple_people` = candidates only. Of the 4,799 short-form agents active in 2023 or later, 553 are high and 157 medium. 1,691 distinct lobbyist person_ids match at high or medium across all years.
- **Member mentions** use `memberlex.find`, title-anchored with the document year. `high` = first + last name; `medium` = unique surname. Lines that are FARA form boilerplate are skipped. The table records *mentions* in statement text, which are mostly contact logs. Some are mass outreach (for example the Korean and Kazakh embassies through Brownstein each list 490+ current members) or subjects of informational materials, so treat it as "documented contact or mention", not "meeting".
- **Foreign principal attribution** (`principal_attribution`): `context_match` = a principal's name or country appears within ±4 lines (medium). `single_active_principal` = the registrant had only one active principal. `registrant_level_only` = not attributable.
- **Contributions**: `high` = the recipient names the member by first and last name ("Robert Aderholt for Congress"). `medium` = a unique surname in campaign framing ("Hoyer for Congress", "Cassidy Leadership Fund"). `unmatched_recipient` = party committees, PACs, state candidates and the like (8,813 rows; kept, with no member link). 11,147 contributions totaling $13.5M link to 675 members (current and former). These are contributions by the registrant, its PAC or its employees, as required by Item 14(c)/15(c). They are not necessarily on a principal's behalf.

## Gaps
- 79 statements are scanned images with no text layer. No OCR was run.
- Exhibit AB, amendments and informational materials were not parsed. Statements before 2023 were not parsed.
- Contact tables that wrap across lines can split a name. Ambiguous surnames are in `fara_ambiguous_member_mentions.csv`.
