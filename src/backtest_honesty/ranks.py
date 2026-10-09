import numpy as np


def rank_tie_order_bug(x):
    return np.argsort(np.argsort(x, kind="stable"), kind="stable").astype(float)


def rank_average(x):
    x = np.asarray(x, float)
    order = np.argsort(x, kind="stable")
    ranks = np.empty(len(x))
    sx = x[order]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and sx[j + 1] == sx[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0
        i = j + 1
    return ranks


def spearman(x, y, rank=rank_average):
    return float(np.corrcoef(rank(np.asarray(x)), rank(np.asarray(y)))[0, 1])
