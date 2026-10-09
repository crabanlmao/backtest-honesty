# backtest-honesty

Checks I run before believing a backtest result.

I have not found a strategy with a proven edge. These tools are how I found that out, and
[docs/BUG_CATALOG.md](docs/BUG_CATALOG.md) lists the 17 mistakes in my own numbers along the way.

| | |
|---|---|
| `search_matched_null` | what the same search finds on shuffled labels |
| `circular_shift_null` | same, for time-clustered data |
| `drop_top_n`, `cluster_bootstrap_ci` | does the mean survive its best trades, is the interval honest about days |
| `delay_profile` | does the edge collapse when the signal is delayed one bar |
| `rank_average` | fixes the `argsort(argsort(x))` tie bug |
| `check_chain` | finds missing records using an exact invariant |

```bash
pip install -e ".[dev]"
python -m pytest
python examples/01_best_of_n_on_noise.py
```

Example output (seeded):

- 19 meaningless features, 800 trades: best filter +2.57 pts, noise median +2.88, p95 +4.61. Not a result.
- Rank correlation of an unrelated feature: +0.54 with the tie bug, -0.03 fixed.
- Lookahead signal: +0.73 at lag 0, +0.01 at lag 1. Honest slow signal: +0.09, +0.08, +0.07.
