"""backtest_honesty: checks that ask "is this result real?" before anyone trades on it."""
from .nulls import search_matched_null, circular_shift_null, band_search
from .robustness import drop_top_n, cluster_bootstrap_ci
from .leakage import delay_profile
from .ranks import rank_tie_order_bug, rank_average, spearman
from .invariants import check_chain

__all__ = [
    "search_matched_null", "circular_shift_null", "band_search",
    "drop_top_n", "cluster_bootstrap_ci", "delay_profile",
    "rank_tie_order_bug", "rank_average", "spearman", "check_chain",
]
