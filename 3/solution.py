"""
Some unreadable one-liner solutions :D
"""

import re
from typing import Iterable, Pattern

EXPECTED_RESULT_PART1: int = 161
EXPECTED_RESULT_PART2: int = 48
MUL_PATTERN: Pattern = re.compile(r"mul\((\d+),(\d+)\)")
MUL_WITH_CONDITIONS_PATTERN: Pattern = re.compile(
    rf"{MUL_PATTERN.pattern}|(do\(\)|don\'t\(\))"
)


def part1(input: Iterable[str]) -> int:
    return sum(
        int(digit1) * int(digit2)
        for row in input
        for digit1, digit2 in MUL_PATTERN.findall(row)
    )


def part2(input: Iterable[str]) -> int:
    can_multiply: bool = True
    return sum(
        int(digit1) * int(digit2)
        for row in input
        for digit1, digit2, condition in MUL_WITH_CONDITIONS_PATTERN.findall(row)
        if (
            (can_multiply := condition == "do()" or (condition == "" and can_multiply))
            and digit1 != ""
            and digit2 != ""
        )
    )
