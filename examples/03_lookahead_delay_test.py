import numpy as np

from backtest_honesty import delay_profile

rng = np.random.default_rng(9)
n = 50_000
state = np.zeros(n)
for t in range(1, n):
    state[t] = 0.9 * state[t - 1] + rng.normal()
ret = 0.05 * state + rng.normal(size=n)

for name, sig in [("honest", state), ("lookahead", ret + rng.normal(scale=0.5, size=n))]:
    out = delay_profile(sig, ret, lags=range(0, 5))
    row = "  ".join(f"lag {k}: {v:+.3f}" for k, v in out["profile"].items())
    print(f"{name:10s} {row}  cliff: {out['suspicious_cliff_at_lag_1']}")
