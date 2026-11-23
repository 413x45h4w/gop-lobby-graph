# Influence map dataset (derived; built 2026-11-21 ET, refreshed 2026-11-22 ET)

Compact dataset behind the interactive "Lobbyist–Congress influence map" Page.

- `build_map_raw.py` selects nodes and edges from money_all/, x_all/ and instagram/ (writes /workspace/mapbuild/raw.json).
- `emit_map.py` adds node attributes, a precomputed spring layout, and writes `influence_map_data.json`.
- `influence_map_data.json`: `n` = node rows (kind L/M/C/B, name, party/lean, attributes..., x, y);
  `e` = space-separated edges `src.dst.type.value` (indices and values in base 36; X values are weight×4).
  Edge types: 0 direct, 1 former staffer, 2 PAC indirect, 3 JFC, 4 lobbyist→committee, 5 PAC officer,
  6 Form 3L bundling, 7 bundler's lobbyists, 8 committee→member, 9 X, 10 Instagram.

Selection: 234 lobbyists (top 120 direct+PAC, top 40 direct-only, top 20 $ to members, GOP-300 combined top 20,
all 88 with accepted X ties, Jeffrey Miller), 396 members, 53 committees, 6 bundlers; per-lobbyist top 6 direct (>=$500),
top 3 PAC-indirect and top 3 JFC (>=$100), top 4 committee (>=$250); committees' top 6 member recipients.

## Refresh log (append-only)

- 2026-11-22 ET: rebuilt against the 2026-11-21 X run (x_edges_all_party.csv 140 rows, 127 weighted) and Instagram batch 5
  (no new member tags; money_all unchanged since 2026-11-18). `emit_map.py` now capitalises hyphenated words.
  `stabilize_map.py <prev map json> <prev raw json>` keeps the previous Page's node order and positions, appends new nodes
  (placed beside their ties) and new edges. Result: 702 nodes (240 L, 403 M, 53 C, 6 B), 2,851 edges (+13 nodes, +51 edges).

## v2: all public DC layers (built 2026-11-22 ET) — `v2/`

Same Page (canvas 10572e4a-64c3-4ddd-9e73-ec0c5658be57), rebuilt to add ld2/, revolving/, fara/, outside_money/, nonprofits/,
boards/, legislative/, executive/, ethics/ and state_events/ on top of money_all/, x_all/ and instagram/ (money layers unchanged).

- `common.py`, `s1_lobbyists.py` … `s6_emit.py`: pipeline (reads ../ layers under full/, writes small pickles to /workspace/mapbuild/v2/,
  not committed). s3 holds the cross-layer score weights; s4 selects drawn vs indexed; s5 builds edges; s6 emits `map_v2.json`.
- `map_v2.json`: `rows` (`kind|name|lean|sub|x36|y36|score10_36|metrics` with metrics base-36 joined by "."; x/y empty = indexed only,
  rows ordered drawn first, `ndrawn`=944), `es` (`src.dst.type.value[.conf]` base 36; conf 1 = medium, 2 = low, absent = high;
  X values ×4), `TYS` (46 edge type names). `map_v2_ids.json` maps rows back to source ids.
- `page_v2.canvas.tsx`: the Page source as published; `verify_page.py <file>` checks a Page source against `map_v2.json`
  (2026-11-22: 1,294 rows and 3,316 edges, 0 mismatches).
- Nodes: 944 drawn (308 M, 257 L, 91 K client, 67 N nonprofit/527/travel sponsor, 55 S super PAC/IE spender, 47 H committee,
  30 W bill, 23 F foreign principal, 18 C, 18 A agency, 17 R FARA registrant, 8 U caucus, 5 B) + 350 indexed only
  (231 M, 67 L, 39 K, 4 A, 2 C, 2 N, 2 H, 1 S, 1 F, 1 B). Edges: 3,316 (3,025 high, 223 medium, 68 low).
- Cross-layer scores are percentile-weighted sums (weights in s3 and on the Page): lobbyists money .35, LD-2 $ .15, clients .05,
  bills .10, revolving door .10, OIRA .05, super PAC .05, FARA .05, testimony .025, 990 boards .025, X .05; members lobbyist $ .30,
  IE .15, ex-staff lobbyists .15, client-sponsored bills .15, FARA .10, travel .05, trades/holdings .05, X .05; clients LD-2 $ .40,
  sponsoring members .15, super PAC .15, OIRA .10, witness .05, travel .05, member holdings/trades .05, bills .05.
- Caveats carried on the Page: WH visitor logs not published by the current administration (Biden-era name matches LOW only);
  regulations.gov comments are a sample; OpenSecrets / FollowTheMoney / Political Party Time unavailable, LegiStorm paywalled;
  990 donors redacted; FARA counts are mentions, not meetings; 990 former-member matches ~75–80% precise (indexed, not drawn);
  Jim Justice's Blackstone Energy holding excluded.
