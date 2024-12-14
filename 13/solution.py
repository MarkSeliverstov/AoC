from __future__ import annotations

import re
from typing import Iterator

EXPECTED_RESULT_PART1: int = 480
EXPECTED_RESULT_PART2: int = 875318608908


def get_machines(text: str) -> Iterator[list[int]]:
    for machine_text in text.split("\n\n"):
        values: list[int] = [int(value) for value in re.findall(r"\d+", machine_text)]
        if len(values) == 6:
            yield values


def min_preses(
    ax: int,
    ay: int,
    bx: int,
    by: int,
    px: int,
    py: int,
    prize_addition: int = 0,
) -> int:
    """
    A * ax + B * bx = px
    A * ay + B * by = py
    """
    px = prize_addition + px
    py = prize_addition + py

    A: float = (bx * py - by * px) / (ay * bx - ax * by)
    B: float = (px - A * ax) / bx
    if A % 1 == B % 1 == 0:
        return int(A * 3 + B)
    return 0


def part1(text: str) -> int:
    return sum(min_preses(*values) for values in get_machines(text))


def part2(text: str) -> int:
    return sum(min_preses(*values, 10000000000000) for values in get_machines(text))
