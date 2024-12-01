from collections import defaultdict
from typing import Iterable, Iterator


def first_part_solution(input: Iterable[str]) -> int:
    left: list[int] = []
    right: list[int] = []

    for row in input:
        splitted_line: list[str] = row.split()
        if len(splitted_line) == 0:
            continue

        if len(splitted_line) != 2:
            raise ValueError(f"Incorrect input: {row=}, {splitted_line=}")
        left.append(int(splitted_line[0]))
        right.append(int(splitted_line[1]))

    left.sort()
    right.sort()
    assert len(left) == len(right)
    result: int = 0
    for l, r in zip(left, right):
        result += abs(l - r)

    return result


def second_part_solution(input: Iterable[str]) -> int:
    left: list[int] = []
    right_frequency: defaultdict[int, int] = defaultdict(int)

    for row in input:
        splitted_line: list[str] = row.split()
        if len(splitted_line) == 0:
            continue

        if len(splitted_line) != 2:
            raise ValueError(f"Incorrect input: {row=}, {splitted_line=}")
        left.append(int(splitted_line[0]))
        right_frequency[int(splitted_line[1])] += 1

    left.sort()
    result: int = 0
    for item in left:
        result += item * right_frequency[item]

    return result


def test_simple_input_data_generator() -> Iterator[str]:
    input: str | None = """3   4
4   3
2   5
1   3
3   9
3   3"""
    for row in input.splitlines():
        yield row