from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

EXPECTED_RESULT_PART1: int = 3749
EXPECTED_RESULT_PART2: int = 11387


Operator = Callable[[int, int], int]


@dataclass(frozen=True)
class Expression:
    expected_result: int
    _remains: list[int]
    _with_operators: list[Operator]

    @staticmethod
    def from_line(line: str, operators: list[Operator]) -> Expression:
        expected_result, values = line.split(":")
        return Expression(
            int(expected_result),
            [int(value) for value in values.split()],
            operators,
        )

    def _is_valid(self, remains: list[int]) -> bool:
        if len(remains) == 1:
            return self.expected_result == remains[0]

        return any(
            self._is_valid([op(remains[0], remains[1])] + remains[2:])
            for op in self._with_operators
        )

    def is_valid(self) -> bool:
        return self._is_valid(self._remains.copy())


def part1(input_lines: Iterable[str]) -> int:
    operators_to_use: list[Operator] = [
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]
    expressions: list[Expression] = [
        Expression.from_line(line, operators_to_use) for line in input_lines
    ]
    return sum(expr.expected_result for expr in expressions if expr.is_valid())


def part2(input_lines: Iterable[str]) -> int:
    operators_to_use: list[Operator] = [
        lambda a, b: a + b,
        lambda a, b: a * b,
        lambda a, b: int(f"{a}{b}"),
    ]
    expressions: list[Expression] = [
        Expression.from_line(line, operators_to_use) for line in input_lines
    ]
    return sum(expr.expected_result for expr in expressions if expr.is_valid())
