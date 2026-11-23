# Influence map v2 (all DC layers) — checkpoint notes
- 2026-11-22 21:20 ET: started. Pulled to 803a890. Reading READMEs.
- 21:30 Read all 10 READMEs. Plan: build_v2.py in /workspace/mapbuild/v2 -> core graph + entity index -> map_v2.json; WriteCanvas same canvas id 10572e4a-...
  Node kinds: L lobbyist, M member, C FEC committee/PAC, S super PAC/IE spender, K client/company, F foreign principal, R FARA registrant, N nonprofit/527, A agency, H cong. committee, W bill, B bundler, U caucus
  Scores: lobbyist DC score (money .35, ld2$ .15, clients .05, bills .10, revolving .10, OIRA .05, superPAC .05, FARA .05, testimony .025, boards/990 .025, X .05)
          member exposure (lobby$ .30, IE .15, ex-staff .15, clients-on-sponsored-bills .15, FARA .10, travel .05, trades/holdings .05, X .05)
          client score (LD2 spend .40, sponsors reached .15, superPAC .15, OIRA .10, witness .05, travel .05, member holdings/trades .05, bills .05)
  Exclude Justice (J000312) BLACKSTONE holding/trade.
- 21:40 s1_lobbyists.py -> s1_lob.pkl, s2_members_orgs.py -> s2.pkl done (Justice Blackstone holding excluded)
- 21:55 s3_score.py (scores) + s4_select.py (Ldraw/Mdraw/Kdraw) done; next s5_graph.py edges+other kinds
- 22:10 s5_graph.py ok: 847 drawn nodes, 4170 edges (need trimming + grants/527 nodes). next s6_emit.py
- 22:30 s6_emit.py -> map_v2.json (rows 108KB, edges 38KB; 944 drawn/1294 indexed/3316 edges). next: headline numbers, then WriteCanvas
- 22:45 page/code.tsx part 1 written (logic); next JSX part
- 22:55 page/code.tsx complete; next assemble + tsc check
- 23:05 page split: w1.tsx (code+ES+RSA) then EditCanvas chunk1..3 into RSB/RSC/RSD
- 23:15 plan: WriteCanvas w0.tsx (code, empty data), then EditCanvas RSA..RSD (rs0-3.txt), ESA/ESB (es0-1.txt, joined by spaces)
- 23:25 WriteCanvas w0 OK (code compiles, empty data). next: EditCanvas RSA (rs0.txt)
- 23:35 RSA edit OK. next RSB (rs1.txt)
- 23:50 RSA+RSB verified 0 mismatches. next RSC (rs2.txt) ; verify via ReadCanvas write_to_file + page/verify.py
- 00:05 RSC edit done (unverified). next RSD (rs3.txt)
- RSD edit done. next ESA/ESB
- ES split into EA0-4/EB0-4 placeholders in canvas; files eA*.txt eB*.txt; EA0 next
- EA0 done
- all data edits done; verifying
- verified 1294/3316 0 mismatch; travel label patched; saved page_v2_final.canvas.tsx. next commit
