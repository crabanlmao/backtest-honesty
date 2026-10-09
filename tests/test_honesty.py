import numpy as np

from backtest_honesty import (
    band_search, search_matched_null, circular_shift_null, drop_top_n, cluster_bootstrap_ci,
    delay_profile, rank_tie_order_bug, rank_average, spearman, check_chain,
)


def test_search_finds_a_positive_result_on_pure_noise_and_the_null_knows():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(400, 15))
    y = rng.normal(size=400)                       # no relationship at all
    out = search_matched_null(lambda yy: band_search(X, yy), y, n_draws=200, seed=2)
    assert out["observed"] > 0                     # the search "found" something
    assert not out["clears_bar"]                   # but it is below what noise produces


def test_search_null_detects_a_real_effect():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(600, 5))
    y = rng.normal(size=600) + 1.5 * (X[:, 2] > 0.5)   # column 2 really matters
    out = search_matched_null(lambda yy: band_search(X, yy), y, n_draws=200, seed=4)
    assert out["clears_bar"]


def test_average_rank_handles_ties_and_matches_known_values():
    assert list(rank_average(np.array([5.0, 1.0, 1.0, 3.0]))) == [3.0, 0.5, 0.5, 2.0]


def test_tie_order_bug_creates_correlation_that_average_rank_removes():
    rng = np.random.default_rng(5)
    n = 2000
    x = np.where(rng.random(n) < 0.9, 0.0, rng.normal(size=n))   # 90% ties, unrelated to y
    y = np.arange(n) / n + rng.normal(scale=0.3, size=n)          # outcome trends with array order
    bug = spearman(x, y, rank=rank_tie_order_bug)
    fixed = spearman(x, y, rank=rank_average)
    assert bug > 0.3
    assert abs(fixed) < 0.1


def test_circular_shift_is_stricter_than_shuffle_on_trending_series():
    rng = np.random.default_rng(6)
    n = 500
    x = np.cumsum(rng.normal(size=n))               # two independent random walks
    y = np.cumsum(rng.normal(size=n))
    corr = lambda a, b: np.corrcoef(a, b)[0, 1]
    shuffled = np.array([corr(x, rng.permutation(y)) for _ in range(500)])
    circ = circular_shift_null(x, y, corr, n_draws=500, seed=7)
    assert circ["null_p95_abs"] > 3 * np.quantile(np.abs(shuffled), 0.95)


def test_drop_top_n():
    r = np.array([100.0, 1, 1, 1, -1, -1, -1, 0, 0, 0])
    out = drop_top_n(r, n=1)
    assert out["mean"] > 9 and out["mean_without_top_1"] < 0.1


def test_cluster_bootstrap_is_wider_than_trade_level_when_days_share_a_market():
    rng = np.random.default_rng(8)
    day = np.repeat(np.arange(20), 30)
    r = np.repeat(rng.normal(size=20), 30) + rng.normal(scale=0.1, size=600)
    lo_c, hi_c = cluster_bootstrap_ci(r, day, n_boot=500)
    lo_t, hi_t = cluster_bootstrap_ci(r, np.arange(600), n_boot=500)
    assert (hi_c - lo_c) > 2 * (hi_t - lo_t)


def test_delay_profile_flags_lookahead_and_passes_a_real_slow_signal():
    rng = np.random.default_rng(9)
    n = 20000
    ret = rng.normal(size=n)
    leak = ret + rng.normal(scale=0.5, size=n)            # signal built from the same bar's return
    assert delay_profile(leak, ret)["suspicious_cliff_at_lag_1"]
    state = np.zeros(n)
    for t in range(1, n):
        state[t] = 0.9 * state[t - 1] + rng.normal()      # persistent state known at t
    ret2 = 0.05 * state + rng.normal(size=n)
    honest = delay_profile(state, ret2)
    assert not honest["suspicious_cliff_at_lag_1"]
    assert honest["profile"][1] > 0.5 * honest["profile"][0]   # fades gradually, no cliff


def test_check_chain_finds_a_missing_record():
    # reserves start at 1000; each record moves the state from pre to post
    state, recs = 1000, []
    for d in [-10, 5, -7, 3, -2]:
        recs.append({"pre": state, "post": state + d})
        state += d
    assert check_chain(recs, lambda r: r["pre"], lambda r: r["post"], start=1000)["breaks"] == []
    broken = recs[:2] + recs[3:]                          # drop the third record
    out = check_chain(broken, lambda r: r["pre"], lambda r: r["post"], start=1000)
    assert len(out["breaks"]) == 1 and out["breaks"][0][0] == 2
