from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

EXPECTED_RESULT_PART1: int = 36
EXPECTED_RESULT_PART2: int = 81


@dataclass
class Map:
    _data: list[str]
    _using_visited: bool
    _visited_nines: defaultdict[tuple[int, int], list[tuple[int, int]]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def get_score(
        self,
        pos_x: int,
        pos_y: int,
        prev_value: int,
        start_x: int,
        start_y: int,
    ) -> int:
        if not (0 <= pos_x < (len(self._data[0])) and 0 <= pos_y < (len(self._data))):
            return 0

        current_value: int = int(self._data[pos_y][pos_x])
        if current_value - prev_value != 1:
            return 0

        if current_value == 9:
            if not self._using_visited:
                return 1

            if (pos_x, pos_y) not in self._visited_nines[(start_x, start_y)]:
                self._visited_nines[(start_x, start_y)].append((pos_x, pos_y))
                return 1
            else:
                return 0

        return sum(
            [
                self.get_score(pos_x + 1, pos_y, current_value, start_x, start_y),
                self.get_score(pos_x, pos_y + 1, current_value, start_x, start_y),
                self.get_score(pos_x - 1, pos_y, current_value, start_x, start_y),
                self.get_score(pos_x, pos_y - 1, current_value, start_x, start_y),
            ]
        )

    def get_all_scores(self) -> int:
        result: int = 0
        for y in range(len(self._data)):
            for x in range(len(self._data[0])):
                if self._data[y][x] == "0":
                    a = sum(
                        [
                            self.get_score(x + 1, y, 0, x, y),
                            self.get_score(x, y + 1, 0, x, y),
                            self.get_score(x - 1, y, 0, x, y),
                            self.get_score(x, y - 1, 0, x, y),
                        ]
                    )
                    result += a
        return result


def part1(input_lines: Iterable[str]) -> int:
    return Map([line.strip() for line in input_lines], True).get_all_scores()


def part2(input_lines: Iterable[str]) -> int:
    return Map([line.strip() for line in input_lines], False).get_all_scores()
