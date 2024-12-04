from dataclasses import dataclass
from enum import Enum
from typing import Iterable

EXPECTED_RESULT_PART1: int = 18
EXPECTED_RESULT_PART2: int = 9


class Direction(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL_1 = 3
    DIAGONAL_2 = 4


@dataclass
class Grid:
    _grid: list[str]

    @staticmethod
    def from_lines(lines: Iterable[str]) -> "Grid":
        return Grid([line.strip() for line in lines])

    def _are_possible_offsets(self, y: int, x: int, dy: int, dx: int) -> bool:
        if (
            (y + dy) >= 0
            and (x + dx) >= 0
            and (y + dy) < len(self._grid)
            and (x + dx) < len(self._grid[0])
        ):
            return True
        return False

    def _there_is_word_from_pos(
        self, y: int, x: int, direction: Direction, is_positive: bool, word: str
    ) -> bool:
        dy, dx = {
            Direction.HORIZONTAL: (0, 1),
            Direction.VERTICAL: (1, 0),
            Direction.DIAGONAL_1: (1, 1),
            Direction.DIAGONAL_2: (1, -1),
        }[direction]
        if not is_positive:
            dy, dx = -dy, -dx

        if not self._are_possible_offsets(
            y, x, dy * (len(word) - 1), dx * (len(word) - 1)
        ):
            return False

        for char in word:
            if self._grid[y][x] != char:
                return False
            y += dy
            x += dx
        return True

    def _get_word_count_for_each_directiond(
        self, y: int, x: int, direction: Direction, is_positive: bool, word: str
    ) -> int:
        result: int = 0
        for direction in Direction:
            for is_positive in [True, False]:
                if self._there_is_word_from_pos(y, x, direction, is_positive, "XMAS"):
                    result += 1
        return result

    def _is_mas_in_X(self, y, x):
        mas_permutations: list[str] = ["MSSM", "MMSS", "SMMS", "SSMM"]
        yx_offsets: list[tuple[int, int]] = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        if not all(self._are_possible_offsets(y, x, dy, dx) for (dy, dx) in yx_offsets):
            return False

        return any(
            all(
                self._grid[y + dy][x + dx] == char
                for (dy, dx), char in zip(yx_offsets, perm)
            )
            for perm in mas_permutations
        )

    def count_xmas(self) -> int:
        result: int = 0
        for i in range(len(self._grid)):
            for j in range(len(self._grid[i])):
                if self._grid[i][j] == "X":
                    result += self._get_word_count_for_each_directiond(
                        i, j, Direction.HORIZONTAL, True, "XMAS"
                    )
        return result

    def count_mas_in_X(self) -> int:
        result: int = 0
        for i in range(len(self._grid)):
            for j in range(len(self._grid[i])):
                if self._grid[i][j] == "A" and self._is_mas_in_X(i, j):
                    result += 1
        return result


def part1(input_lines: Iterable[str]) -> int:
    return Grid.from_lines(input_lines).count_xmas()


def part2(input_lines: Iterable[str]) -> int:
    return Grid.from_lines(input_lines).count_mas_in_X()
