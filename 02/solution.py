from typing import Iterable, Iterator

EXPECTED_RESULT_PART1: int = 2
EXPECTED_RESULT_PART2: int = 4


def _is_safe(levels: list[int]) -> bool:
    if abs(levels[0] - levels[1]) > 3:
        return False

    is_decrease: bool = levels[0] > levels[1]
    for i in range(1, len(levels)):
        diff: int = abs(levels[i - 1] - levels[i])
        if not (1 <= diff <= 3 and (levels[i - 1] > levels[i]) == is_decrease):
            return False

    return True


def _generate_toleranced_rows(row: list[str]) -> Iterator[list[int]]:
    for i in range(len(row)):
        yield [int(row[j]) for j in range(len(row)) if j != i]


def part1(input: Iterable[str]) -> int:
    return sum(1 for row in input if _is_safe([int(i) for i in row.split()]))


def part2(input: Iterable[str]) -> int:
    return sum(
        1
        for row in input
        if any(
            _is_safe(row_toleranced)
            for row_toleranced in _generate_toleranced_rows(row.split())
        )
    )
