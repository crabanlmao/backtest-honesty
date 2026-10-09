import numpy as np


def delay_profile(signal, forward_returns, lags=range(0, 6)):
    s = np.sign(np.asarray(signal, float))
    r = np.asarray(forward_returns, float)
    prof = {}
    for lag in lags:
        prof[lag] = float(np.mean(s * r)) if lag == 0 else float(np.mean(s[:-lag] * r[lag:]))
    base, nxt = prof[0], prof.get(1, 0.0)
    cliff = bool(base > 0 and (nxt <= 0 or base / max(nxt, 1e-12) > 5))
    return {"profile": prof, "suspicious_cliff_at_lag_1": cliff}
