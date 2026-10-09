import numpy as np


def band_search(X, y, quantiles=np.linspace(0.05, 0.95, 19)):
    base = y.mean()
    best = -np.inf
    for j in range(X.shape[1]):
        col = X[:, j]
        for q in quantiles:
            kept = y[col > np.quantile(col, q)]
            if len(kept) >= 10:
                best = max(best, kept.mean() - base)
    return float(best)


def search_matched_null(search_fn, y, n_draws=1000, seed=0):
    rng = np.random.default_rng(seed)
    observed = float(search_fn(y))
    draws = np.array([search_fn(rng.permutation(y)) for _ in range(n_draws)])
    return {
        "observed": observed,
        "null_median": float(np.median(draws)),
        "null_p95": float(np.quantile(draws, 0.95)),
        "p_value": float((1 + np.sum(draws >= observed)) / (n_draws + 1)),
        "clears_bar": bool(observed > np.quantile(draws, 0.95)),
    }


def circular_shift_null(x, y, stat, n_draws=1000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(y)
    observed = float(stat(x, y))
    draws = np.array([stat(x, np.roll(y, int(rng.integers(1, n)))) for _ in range(n_draws)])
    bar = float(np.quantile(np.abs(draws), 0.95))
    return {
        "observed": observed,
        "null_median_abs": float(np.median(np.abs(draws))),
        "null_p95_abs": bar,
        "clears_bar": bool(abs(observed) > bar),
    }
