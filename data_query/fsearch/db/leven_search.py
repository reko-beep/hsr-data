from Levenshtein import ratio


def fsearch(entry, choices) -> str | None:
    cutoff: float = 0.1
    candidates = {}

    for i in choices:
        score: float = ratio(entry, i)
        if score > cutoff:
            candidates[i] = score
    print(choices)
    print(candidates)
    try:
        return max(candidates, key=candidates.__getitem__)
    except ValueError:
        return None
