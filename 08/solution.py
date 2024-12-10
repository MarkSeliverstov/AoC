"""
Antinodes conditions:
    1. The two antennas and the antinode must lie on the same line
    ( (x2-x1)(y2-y1) == (x3-x2)(y3-y3)  for 3 points (x1, y1), (x2, y2), (x3, y3) )
    2. One of the antennas is twice as far away as the other from tha ANTINODE.
    (if A-antinode, N1-antenna1, N2-antenna2, then Distance(A, N1) = 2 * Distance(A, N2))
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

EXPECTED_RESULT_PART1: int = 14
EXPECTED_RESULT_PART2: int = 34


@dataclass(eq=True, frozen=True)
class Postition:
    x: int
    y: int

    def get_possible_antinode_positions(
        self, other: Postition, multiplicator: int = 1
    ) -> list[Postition]:
        dX: int = other.x - self.x
        dY: int = other.y - self.y
        if dX == 0 and dY == 0:
            return [Postition(self.x, self.y)]

        return [
            Postition(other.x + dX * multiplicator, other.y + dY * multiplicator),
            Postition(self.x - dX * multiplicator, self.y - dY * multiplicator),
        ]


@dataclass
class Map:
    _data: list[str]
    _hight: int
    _widht: int
    _antinodes_for_whole_line: bool

    @staticmethod
    def from_lines(data: list[str], antinodes_for_whole_line: bool = False) -> Map:
        return Map(data, len(data), len(data[0]), antinodes_for_whole_line)

    def _get_antinodes_for_new_antena(
        self, new_antena: Postition, existed_antenas: set[Postition]
    ) -> set[Postition]:
        if not self._antinodes_for_whole_line:
            return set(
                antinode
                for node in existed_antenas
                for antinode in new_antena.get_possible_antinode_positions(node)
                if (0 <= antinode.x < self._widht and 0 <= antinode.y < self._hight)
            )
        else:
            new_antinodes: set[Postition] = set()
            for node in existed_antenas:
                multiplicator: int = 0
                while True:
                    continuing: bool = False
                    for possible_antinode in new_antena.get_possible_antinode_positions(
                        node, multiplicator
                    ):
                        if (
                            0 <= possible_antinode.x < self._widht
                            and 0 <= possible_antinode.y < self._hight
                        ):
                            new_antinodes.add(possible_antinode)
                            continuing = True
                    if not continuing:
                        break
                    multiplicator += 1
            return new_antinodes

    def get_antinodes_count(self) -> int:
        seen_antenas: defaultdict[str, set[Postition]] = defaultdict(set)
        seen_antinode: set[Postition] = set()
        for y in range(self._hight):
            for x in range(self._widht):
                cell: str = self._data[y][x]
                if cell != ".":
                    antena_pos: Postition = Postition(x, y)
                    seen_antinode.update(
                        self._get_antinodes_for_new_antena(
                            antena_pos, seen_antenas[cell]
                        )
                    )
                    seen_antenas[self._data[y][x]].add(Postition(x, y))
        return len(seen_antinode)


def part1(input_lines: Iterable[str]) -> int:
    return Map.from_lines([line.strip() for line in input_lines]).get_antinodes_count()


def part2(input_lines: Iterable[str]) -> int:
    return Map.from_lines(
        [line.strip() for line in input_lines], True
    ).get_antinodes_count()
