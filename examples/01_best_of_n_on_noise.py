import numpy as np

from backtest_honesty import band_search, search_matched_null

rng = np.random.default_rng(2026)
X = rng.normal(size=(800, 19))
y = rng.normal(scale=10.0, size=800)

res = search_matched_null(lambda yy: band_search(X, yy), y, n_draws=500, seed=1)
print(f"best filter on real labels: {res['observed']:+.2f} pts/trade")
print(f"same search on shuffled labels: median {res['null_median']:+.2f}, p95 {res['null_p95']:+.2f}")
print(f"clears the bar: {res['clears_bar']}")
