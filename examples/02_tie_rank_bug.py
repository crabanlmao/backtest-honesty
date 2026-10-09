import numpy as np

from backtest_honesty import rank_average, rank_tie_order_bug, spearman

rng = np.random.default_rng(5)
n = 2000
x = np.where(rng.random(n) < 0.9, 0.0, rng.normal(size=n))
y = np.arange(n) / n + rng.normal(scale=0.3, size=n)

print(f"ties broken by position: {spearman(x, y, rank=rank_tie_order_bug):+.3f}")
print(f"ties share a rank:       {spearman(x, y, rank=rank_average):+.3f}")
