# Selection rules: top 300 GOP-aligned registered lobbyists (computed 2026-11-17, EST)
Source: every LD-2 quarterly report on lda.gov, 2022Q4–2026Q3 (lda/ld2_universe, about 310k filings), and every LD-203 report, 2023 mid-year through 2026 mid-year (lda/ld203_universe). Scripts: select300.py, then merge_people.py.
1. **Universe.** Lobbyists listed on outside-firm LD-2 reports that disclose income, 2023Q1–2026Q3. In-house registrants report expenses rather than income, so they are excluded.
2. **Attributable income.** Each filing's income is split equally among the distinct lobbyists listed on it, then summed for 2023–26. This is a heuristic: LDA does not apportion income to individuals.
3. **Person merge.** LDA lobbyist IDs belonging to the same person are merged. The rule is same name AND (covered-position token Jaccard ≥0.4 OR the registrants share a first word, e.g. POLARIS / POLARIS-HUTTON). 273 groups were merged; 26 of them are in the top 300. Same-name people with different covered positions are kept separate (e.g. David Stewart ×2).
4. **GOP signals (at least one required):**
   - S1: works at a GOP-identified firm (Ballard, Miller Strategies, Continental Strategy, CGCN, Checkmate, Michael Best Strategies, Cove Strategies).
   - S2: the covered-position text names more Republican than Democratic legislators or entities (lexicon of every legislator since 1990, plus party keywords).
   - S3: LD-203 FECA giving that is ≥67% to Republicans and ≥$2,000 to Republicans.
   - S4: the lobbyist is a former Republican member of Congress.
5. **Disqualifiers (any one excludes):** the covered position leans Democratic (unless S4 applies); a former Democratic member; LD-203 giving ≤33% Republican with ≥$2,000 to Democrats.
6. **Rank and cut.** Eligible people are ranked by attributable income and the top 300 are taken. Cutoff: $4.12M. Eligible pool: 2,185 of 8,159 people with income.
   - Signal counts in the 300: S3 280, S2 166, S1 34, S4 6.
