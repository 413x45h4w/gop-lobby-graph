# Influence map dataset (derived, 2026-11-21 ET)

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
