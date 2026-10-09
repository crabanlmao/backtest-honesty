def check_chain(records, pre, post, start=None):
    breaks, prev, n, first = [], None, 0, None
    for i, r in enumerate(records):
        p = pre(r)
        if prev is None:
            first = p
        elif p != prev:
            breaks.append((i, prev, p))
        prev = post(r)
        n += 1
    return {"n": n, "breaks": breaks, "starts_at_start": (first == start) if start is not None else None}
