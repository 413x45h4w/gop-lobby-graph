# /workspace/gop-lobby-graph (pilot, created 2026-11-17 EST; append-only raw logs)
- PILOT_REPORT.md: findings, coverage, budget and full-build plan
- pilot_network.png: network plus a chart of X visibility vs LD-203 money ties
- pilot_lobbyist_ranking.csv: 15 lobbyists with social metrics, PageRank, LDA sample counts and LD-203 matches
- pilot_edges_posts.csv: one row per (post, member, lobbyist), with URL, date, type, era, snippet and needs_review
- pilot_edges_weighted.csv: aggregated member-lobbyist pairs (lobbying era)
- pilot_ld203_contributions.csv, ld203_summary.json: LD-203 FECA items with GOP-member name matches
- lda_firm_income_2025.csv: firm LD-2 income for firms fully fetched so far
- nodes_gop_members.csv, pilot_lobbyists.json: node lists, handles and confidence levels
- pilot_queries.json, x_call_log.csv, x_posts_raw.jsonl: exact queries, call log and raw posts (append-only)
- lda/: LDA raw pulls (append-only jsonl). The fetch_lda.py firm crawl may still be running in the background.
- bluesky/: Bluesky actor-search feasibility sample
- Scripts: ingest.py, build_graph.py (classifier rules_v2), rank_and_plot.py, ld203_match.py
No images are stored. People are identified only from captions, @tags and alt text.
