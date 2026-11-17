# GOP members × GOP-aligned lobbyists social graph — FEASIBILITY PILOT
Generated 2026-11-17 ~12:15 PM EST. The data files are append-only and each row carries a timestamp. Window: Nov 17 2022 – Nov 17 2026.

## Bottom line
Using X alone, a photo and shout-out graph does not measure lobbyist influence. It mostly measures who is active on X.
- 9 of the 15 pilot lobbyists have zero lobbying-era edges. That includes the top earners: Brian Ballard, whose firm took in $88.1M in 2025 per LDA, plus David Urban (BGR), Bryan Lanza (Mercury), Ches McDowell (Checkmate) and Marc Lampkin (Brownstein). Their exact-name X accounts have 0 posts, or no account could be found.
- Matt Schlapp accounts for 216 of the 226 lobbying-era post-edges. He links to 67 GOP members and appears in 22 photo-together posts. Almost all of this comes from his CPAC chair role (ratings awards and CPAC events), not from Cove Strategies lobbying.
- LD-203 disclosures run the opposite way. Ed Royce reported FECA contributions to 93 current GOP members ($410k, 2023–26). Greg Walden reported 74 ($180k) and Marc Lampkin 53 ($132.5k). None of the three has a single lobbying-era X edge.

## Method
- **Nodes, members:** 274 current Republican members (119th Congress) from unitedstates/congress-legislators. 257 have official X handles; I added 12 manually and verified them with get_users_by_usernames. Wikidata P2002 added 134 alternate handles (personal and campaign) for 124 members.
- **Nodes, lobbyists:** each pilot lobbyist was confirmed in LDA (lda.gov API; lda.senate.gov returns 503) as named on 2023–26 filings. Their X handles were checked, with a confidence level recorded in pilot_lobbyists.json.
- **Edges:** X full-archive search (`search_posts_all`), -is:retweet, start Nov 17 2022, using four query families:
  - A: members' official handles posting @lobbyist or the lobbyist's full name (11 chunks).
  - A_alt: the same for members' alternate handles (6 chunks).
  - B: lobbyists posting @member, official and alternate handles (10 chunks).
  - C: lobbyists' image posts that use a title (Senator/Congressman/Rep./Speaker…), name-matched to members.
- **People are identified only from caption text, @tags and alt text.** There is no image or face analysis.
- **Classifier (rules_v2):**
  - photo_together: photo plus a co-presence cue such as with / great to see / joined us / welcome / met with / presented me.
  - photo_probable_award: photo plus an award or honor cue.
  - photo_mention_unclear, shoutout, reply (counterpart only in the leading reply @-run), list_mention (8 or more @s), video_or_gif_mention, mention_other.
  - Weights are 3 / 2 / 1.5 / 1 / 1 / 0.5 / 0.5 / 0.25.
- **Era filter:** posts before a lobbyist left Congress or registered count as "colleague_era" and are excluded from the ranking (Bucshon before Jan 4 2025, Burr before 2025). "Connie Mack" without "IV" is marked ambiguous and excluded, since it can also mean Connie Mack III. Posts made before the member entered Congress are flagged (member_status_at_post).
- **Ranking:** weighted degree, distinct members, distinct members who authored the post, photo counts and PageRank on the weighted bipartite graph. These are cross-referenced with LDA filing counts and LD-203 FECA contributions name-matched to current GOP members.

## Coverage and budget
- **X reads:** about 48 requests out of the 1,000/day cap (43 searches and 5 user lookups). Peak use was about 10 a minute.
- **Full archive:** works back to Nov 2022 with from:, @ and has:images. Queries can be up to 1,024 characters (about 25 from: handles or 45 @handles per query).
- **Paging:** 8 of 8 paging tests returned an empty page 2 whenever page 1 had fewer than 25 results. So most chunks cost one call, and only dense chunks (Schlapp) needed 2–3.
- **Totals:** 294 posts retrieved, 268 post-edges, of which 226 are lobbying-era. That gives 75 member–lobbyist pairs.
- **Recall gap:** a check on "@mschlapp CPAC award" found that RussellFrySC (Rep. Fry's personal account) posted an award photo the official-only list missed. That is why I added the Wikidata alternate handles. Leadership accounts such as @SpeakerJohnson are not in either list; I mapped SpeakerJohnson by hand.
- **Precision:** I read the 23 lobbying-era photo_together captions by hand. About 12 clearly show co-presence, about 5 probably do and about 6 are uncertain, so precision is roughly 50–75%. Every photo row has needs_review=True.

## Other platforms
- **Bluesky:** the public API works without a login. In a sample of 30 GOP members, none had an identifiable account (all hits were other people). None of the 15 lobbyists was confirmed; only empty placeholder accounts with matching names turned up. Not worth including.
- **Instagram, Facebook, Threads:** this is where the "great to see X" photo posts mostly live, but there is no public search API. Meta's Content Library is approval-only for researchers, and scraping would mean getting around logins, which is off-limits.
- **LinkedIn:** public profiles need a login, and there is no posts API for third parties. Off-limits.
- **Recommendation:** only X, Bluesky and LDA/FEC are realistically accessible under the rules.

## Top pilot findings
These are lobbying-era edges with post links.
- **Schlapp ↔ Jim Jordan** (20 posts, 2 photo-together), e.g. the 2024 CPAC ratings reception "Over 70 members came…": https://x.com/mschlapp/status/1793660244981129358 and Nov 10 2026 "next Republican Leader": https://x.com/mschlapp/status/2120258780802036015
- **Schlapp ↔ Mike Lee** (29 posts; 16 are one Jan 29 2026 reply thread by @BasedMikeLee, which shows reply threads inflate counts and should be capped per conversation in the full build). **Schlapp ↔ Stefanik** (9). **Schlapp ↔ Speaker Johnson** (7), e.g. "joined us at the Museum of the Bible": https://x.com/mschlapp/status/1983704686084432221
- **Members posting award photos** that tag @mschlapp: Cramer https://x.com/SenKevinCramer/status/1681763408973115392, Griffith https://x.com/RepMGriffith/status/1794471325542568410, Kustoff https://x.com/RepDavidKustoff/status/1794047228686016709
- **Schlapp with Reps. Hamadeh and Davidson** at CPAC Hungary: https://x.com/mschlapp/status/1928026025793048614
- **Carlos Trujillo ↔ Jimmy Patronis:** a birthday photo post https://x.com/JimmyPatronis/status/1761180836555063678 and a Continental hire shout-out https://x.com/JimmyPatronis/status/1857366982032507226. Both are from 2024, before Patronis entered Congress.
- **Connie Mack IV ↔ Rick Scott:** https://x.com/ConnieMackIV/status/1875395002337259540 and Scott's photo with "former Representative Connie Mack IV": https://x.com/SenRickScott/status/1875236880377168306
- **Larry Bucshon:** all 37 edges are from his time as a member, so none count for lobbying-era influence.

## Biases
1. Most top lobbyists don't post, so X visibility runs against discretion and against money.
2. Staff run members' accounts, and official accounts avoid tagging lobbyists, which raises ethics and optics concerns.
3. Schlapp-type nodes, who hold a media or activist role alongside registration, dominate.
4. Tag ambiguity: "Connie Mack" and title+surname collisions. Common names such as Jeff Miller (Miller Strategies) or Chris Stewart can't be searched by name.
5. Personal and campaign accounts are only partly covered, and Wikidata handles can be stale.
6. The search index can drop deleted or protected posts, and it does not expose photo tags of untagged people.
7. Colleague-era edges for ex-members inflate their numbers unless filtered.
8. LD-203 name matching is approximate, and it counts all FECA items the lobbyist reported (some via PACs).

## Projected full build
- **Nodes:** about 274 members (about 400 handles) × N lobbyists.
- **Cost per block of about 15 lobbyists:** roughly 17 A-chunks, 10 B-chunks and 2–3 C pages, about 40 calls with paging.
- **Total calls:**
  - 300 lobbyists (about 20 blocks): ~800 calls, 1 day at the cap.
  - 1,000 lobbyists: ~2,700 calls, 3 days.
  - 3,000 lobbyists: ~8,000 calls, 8+ days.
- **Handle discovery:** usually the bigger cost. Batch get_users_by_usernames (30 usernames per call worked) plus web search, with about 10–20% of lobbyists having active accounts.
- **Agent time:** each call is a separate agent tool call, about 10–20 s each. 800 calls is about 3–5 agent-hours plus parsing.

## Recommended plan
1. Reframe the influence model so LDA/FEC is the backbone:
   - LDA income and client counts.
   - LD-203 contributions and honoraria to members.
   - Covered positions (ex-staff of member X lobbying member X).
   - FEC Schedule A itemized giving and bundling (LD-203 and FEC host committees).
   - X edges as a secondary "public affinity" layer.
2. Nodes: lobbyists from complete LDA pulls of the top ~40 GOP-aligned firms (the fetch has started: 8 of 30 firms were done as of about 12:20 PM EST in lda/lda_filings_2025_2026.jsonl), plus all former members and staff with covered positions.
3. X: run the A/A_alt query families with name terms for every lobbyist, since members name lobbyists more often than they tag them. Run B/C only for lobbyists with active handles. Add leadership and committee accounts.
4. Classification: hand-review every photo edge (caption only), or use an LLM pass on captions with a sample audit.
5. Metrics: weighted degree, distinct members, member-authored breadth, PageRank, and a combined index alongside LD-203 and FEC money ties. Report X-only and money-only rankings separately.
