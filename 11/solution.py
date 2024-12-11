from functools import cache
from typing import Iterable

EXPECTED_RESULT_PART1: int = 55312
EXPECTED_RESULT_PART2: int = 65601038650482


@cache
def blink(value: int, times: int) -> int:
    if times == 0:
        return 1
    if value == 0:
        return blink(1, times - 1)

    val_str: str = str(value)
    if len(val_str) % 2 == 0:
        left: int = int(val_str[: len(val_str) // 2])
        right: int = int(val_str[len(val_str) // 2 :])
        return blink(left, times - 1) + blink(right, times - 1)

    return blink(value * 2024, times - 1)


def part1(input_lines: Iterable[str]) -> int:
    return sum(blink(int(value), 25) for value in list(input_lines)[0].strip().split())


def part2(input_lines: Iterable[str]) -> int:
    return sum(blink(int(value), 75) for value in list(input_lines)[0].strip().split())
