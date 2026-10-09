# 17 mistakes in my own numbers

From memecoin research on Solana and an Ethereum L2, July to October 2026. The data is private, so the
numbers can't be re-run from here. Nearly all of these pushed results up.

| # | Mistake | Effect | Caught by |
|---|---|---|---|
| 1 | Buys that never landed counted as open positions | 85 of 103 "unpriceable" closes were phantoms booked at +299% | reconciling against on-chain fills |
| 2 | Price computed as vSOL²/K with K assumed constant | returns inflated (+356% shown for a +111% move); K drifted a median 82% inside one position | pricing from reserves, checked against traders' own fills: median ratio 0.998 |
| 3 | A sanity floor silently dropped ticks | 15,524 ticks over 508 positions, the crashes | asking why "silent" coins were trading |
| 4 | A clamp booked a crash to 17 as an exit at 30 | losses shrunk | reading the fix's neighbours |
| 5 | Positions that never sold booked at the last price looked at | 83% of the book had no real exit | separating sold from marked |
| 6 | "Truncated" defined by the last tick | 34-54% of coins dropped, mostly the dead ones | defining it against the collection window |
| 7 | Rate-limit 429 returned as an empty result | 5 of 10 test coins read empty | raising on non-success |
| 8 | Trades detected by account list | found 1 in 40; aggregators hide the rest | independent count |
| 9 | Transaction logs cut at 10 KB | 41 of 275 trades missing on one coin | chain continuity check |
| 10 | `argsort(argsort(x))` ties | correlation from tie-breaking only | average ranks |
| 11 | `mktime - timezone` in summer time | coins pulled while still trading | comparing file times with window end |
| 12 | Tape set chosen because a trader later bought those coins | copy bot +19.1 SOL there, -4.4 on an unbiased sample | universe independent of future actions |
| 13 | Wallets selected on being active in the scoring window | -2.7 SOL became +3.3 | past-only eligibility |
| 14 | An execution multiplier borrowed from a faster trader | a branch worth +37.85 SOL was +30.04 | writing down whose execution a constant measured |
| 15 | Other people's simulated transactions in a public log feed | corrupted reserve chains | dropping all-ones signatures |
| 16 | Two coins weighted x10 | 22 of the 24 SOL a filter lost | drop-top-3 and unweighted part |
| 17 | Best of 19 features x 132 cuts on ~2,900 coins | noise median +4.91, p95 +6.50; best real feature +5.04, 55th percentile of its null | `search_matched_null` |
