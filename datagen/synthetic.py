"""Synthetic keys and query workloads.  *** YOU IMPLEMENT THIS FILE. ***

Real data (Spotify) shows how the indexes behave on realistic keys.
Synthetic data lets you control one variable at a time: how many keys, what
order they arrive in, how many lookups hit vs miss, how wide a range is.

Rules for every function:

* Use ``rng = random.Random(seed)`` and draw all randomness from ``rng``, so
  the same seed always produces the same output (on any machine).
* Never modify the list you are given; return a new one.

``tests/test_synthetic.py`` checks each function against this spec. Run it
with ``make test``.
"""

from __future__ import annotations

import random
import string
from typing import Any, Optional, Sequence


def random_keys(
    n: int,
    length: int = 8,
    alphabet: str = string.ascii_lowercase,
    seed: Optional[int] = None,
) -> list[str]:
    """Return ``n`` *distinct* random strings, each exactly ``length`` characters
    long, using only characters from ``alphabet``, in random order.

    Raise ``ValueError`` if ``n`` is larger than the number of possible
    strings (``len(alphabet) ** length``).

    """

    rng = random.Random(seed)

    if n > len(alphabet) ** length:
        raise ValueError("Too many unique keys requested")

    result = []
    seen = set()

    while len(result) < n:
        key = "".join(
            rng.choice(alphabet) for _ in range(length)
        )

        if key not in seen:
            seen.add(key)
            result.append(key)

    return result

     


   



    
    
    

def arrange(
    keys: Sequence[Any],
    order: str,
    seed: Optional[int] = None,
    swap_fraction: float = 0.05,
) -> list[Any]:
    """Return a new list holding the same keys in the requested order.

    order:
        "random"        shuffled
        "sorted"        ascending
        "reversed"      descending
        "nearly_sorted" ascending, then ``round(swap_fraction * len(keys))``
                        swaps of two randomly chosen positions

    Raise ``ValueError`` for any other ``order``.
    """

    rng = random.Random(seed)
    result = list(keys)

    if order == "random":
        rng.shuffle(result)

    elif order == "sorted":
        result.sort()

    elif order == "reversed":
        result.sort(reverse=True)

    elif order == "nearly_sorted":
        result.sort()

        for _ in range(round(swap_fraction * len(result))):
            i = rng.randrange(len(result))
            j = rng.randrange(len(result))
            result[i], result[j] = result[j], result[i]

    else:
        raise ValueError("Unknown order")

    return result





def point_queries(
    keys: Sequence[str],
    n_queries: int,
    hit_rate: float,
    seed: Optional[int] = None,
) -> list[str]:
    """Return ``n_queries`` lookup keys in random order.

    Exactly ``round(n_queries * hit_rate)`` of them are *hits*: chosen at
    random (repeats allowed) from ``keys``. The rest are *misses*: random
    strings that are guaranteed NOT to be in ``keys``, each the same length as
    a randomly chosen key from ``keys``.
    """
    
    rng = random.Random(seed)
    known = set(keys)

    n_hits = round(n_queries * hit_rate)

    result = [
        rng.choice(keys) for _ in range(n_hits)
    ]

    alphabet = string.ascii_letters + string.digits + " _-"

    while len(result) < n_queries:
        length = len(rng.choice(keys))

        candidate = "".join(
            rng.choice(alphabet) for _ in range(length)
        )

        if candidate not in known:
            result.append(candidate)

    rng.shuffle(result)

    return result



def range_queries(
    keys: Sequence[Any],
    n_queries: int,
    selectivity: float,
    seed: Optional[int] = None,
) -> list[tuple[Any, Any]]:
    """Return ``n_queries`` ranges ``(lo, hi)`` for ``index.range_search(lo, hi)``.

    Let ``d`` be the number of *distinct* keys and ``w = max(1, round(selectivity * d))``.
    Sort the distinct keys, pick a random starting position that leaves room
    for ``w`` keys, and use the key there as ``lo`` and the key ``w - 1``
    positions later as ``hi``. So exactly ``w`` distinct keys satisfy
    ``lo <= key <= hi``. Works for any comparable keys (strings or numbers).
    """
    
    rng = random.Random(seed)

    distinct = sorted(set(keys))
    d = len(distinct)

    width = max(1, round(selectivity * d))
    result = []

    for _ in range(n_queries):
        start = rng.randrange(d - width + 1)

        lo = distinct[start]
        hi = distinct[start + width - 1]

        result.append((lo, hi))

    return result



def prefix_queries(
    keys: Sequence[str],
    n_queries: int,
    prefix_length: int,
    seed: Optional[int] = None,
) -> list[str]:
    """Return ``n_queries`` prefixes for ``index.prefix_search(prefix)``.

    Each prefix is the first ``prefix_length`` characters of a randomly chosen
    key that is at least ``prefix_length`` characters long, so every prefix
    matches at least one key.
    """
    
    rng = random.Random(seed)

    eligible = [
        key for key in keys
        if len(key) >= prefix_length
    ]

    result = [
        rng.choice(eligible)[:prefix_length]
        for _ in range(n_queries)
    ]

    return result

