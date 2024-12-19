from __future__ import annotations

from functools import cache

EXPECTED_RESULT_PART1: int = 6
EXPECTED_RESULT_PART2: int = 16


@cache
def is_possible(current: str, result: str, existing_towels: tuple[str]) -> bool:
    if current == result:
        return True
    if not result.startswith(current) or len(current) > len(result):
        return False
    return any(
        is_possible(current + next, result, existing_towels) for next in existing_towels
    )


@cache
def is_possible_count(current: str, result: str, existing_towels: tuple[str]) -> int:
    if current == result:
        return 1
    if not result.startswith(current) or len(current) > len(result):
        return 0
    return sum(
        is_possible_count(current + next, result, existing_towels)
        for next in existing_towels
    )


def part1(input: str) -> int:
    existing_towels_string, results = input.split("\n\n")
    existing_towels: tuple[str, ...] = tuple(existing_towels_string.split(", "))
    return sum(
        1 if is_possible("", result, existing_towels) else 0
        for result in results.split()
    )


def part2(input: str) -> int:
    existing_towels_string, results = input.split("\n\n")
    existing_towels: tuple[str, ...] = tuple(existing_towels_string.split(", "))
    return sum(
        is_possible_count("", result, existing_towels) for result in results.split()
    )
