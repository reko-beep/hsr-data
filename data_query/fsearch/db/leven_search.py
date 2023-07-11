from Levenshtein import ratio


def fsearch(entry, choices):
    cutoff = 0.55
    candidates = {}

    for i in choices:
        score = ratio(entry, i)
        if score > cutoff:
            candidates[i] = score

    try:
        return max(candidates, key=candidates.get)
    except ValueError:
        pass
