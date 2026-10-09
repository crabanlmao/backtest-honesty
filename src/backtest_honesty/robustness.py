import numpy as np


def drop_top_n(returns, n=3):
    r = np.asarray(returns, float)
    top = np.sort(r)[::-1]
    total = r.sum()
    return {
        "mean": float(r.mean()),
        f"mean_without_top_{n}": float(top[n:].mean()) if len(r) > n else float("nan"),
        "share_of_total_from_top_n": float(top[:n].sum() / total) if total != 0 else float("nan"),
    }


def cluster_bootstrap_ci(returns, cluster, n_boot=2000, seed=0, alpha=0.05):
    rng = np.random.default_rng(seed)
    r = np.asarray(returns, float)
    c = np.asarray(cluster)
    groups = [r[c == g] for g in np.unique(c)]
    means = np.empty(n_boot)
    for i in range(n_boot):
        pick = rng.integers(0, len(groups), len(groups))
        means[i] = np.concatenate([groups[k] for k in pick]).mean()
    return float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))
