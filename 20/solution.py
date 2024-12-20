from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import NamedTuple

EXPECTED_RESULT_PART1: int = 44
EXPECTED_RESULT_PART2: int = 0


class Position(NamedTuple):
    y: int
    x: int

    def step(self, dy: int, dx: int) -> Position:
        return Position(y=self.y + dy, x=self.x + dx)


class Cheat(NamedTuple):
    from_pos: Position
    to_pos: Position
    cost: int = 2


@dataclass
class Map:
    _data: list[list[str]]
    start: Position
    end: Position

    @staticmethod
    def from_input(input: str) -> Map:
        start: Position | None = None
        end: Position | None = None
        data: list[list[str]] = [
            [char for char in line] for line in input.strip().split("\n")
        ]
        for y in range(len(data)):
            for x in range(len(data[0])):
                if data[y][x] == "S":
                    start = Position(y=y, x=x)
                if data[y][x] == "E":
                    end = Position(y=y, x=x)
        assert start
        assert end
        return Map(data, start, end)

    def race_without_cheats(self) -> dict[Position, int]:
        current_pos: Position = self.start
        seconds_by_position: dict[Position, int] = {}
        seconds: int = 0
        while current_pos != self.end:
            seconds_by_position[current_pos] = seconds
            for dy, dx in ((1, 0), (-1, 0), (0, -1), (0, 1)):
                next_pos: Position = current_pos.step(dy, dx)
                if (
                    self._data[next_pos.y][next_pos.x] != "#"
                    and next_pos not in seconds_by_position
                ):
                    current_pos = next_pos
                    seconds += 1
                    break
        seconds_by_position[self.end] = seconds
        return seconds_by_position

    def get_possible_cheats_from(
        self, from_pos: Position, max_cheat_cost: int, already_created: set[Cheat]
    ) -> set[Cheat]:
        cheats: set[Cheat] = set()
        max_width: int = len(self._data)
        max_hight: int = len(self._data[0])
        for dx in (-1, 1):
            for i in range(max_cheat_cost + 1):
                for dy in (-1, 1):
                    for j in range(max_cheat_cost - i + 1):
                        if i == j == 0:
                            continue
                        next_step: Position = from_pos.step(dy * j, dx * i)
                        if (
                            0 < next_step.y < max_hight - 1
                            and 0 < next_step.x < max_width - 1
                            and self._data[next_step.y][next_step.x] != "#"
                            and Cheat(next_step, from_pos, i + j) not in already_created
                        ):
                            cheats.add(Cheat(from_pos, next_step, i + j))
        return cheats

    def get_possible_cheats(self, max_cheat_cost: int) -> set[Cheat]:
        possible_cheats: set[Cheat] = set()
        for y in range(len(self._data)):
            for x in range(len(self._data[0])):
                if self._data[y][x] != "#":
                    possible_cheats.update(
                        self.get_possible_cheats_from(
                            Position(y=y, x=x), max_cheat_cost, possible_cheats
                        )
                    )
        return possible_cheats

    def count_possible_cheats(
        self, speedup_more_than: int, max_possible_cheats: int
    ) -> int:
        original_race_stats: dict[Position, int] = self.race_without_cheats()
        possible_cheats: set[Cheat] = self.get_possible_cheats(max_possible_cheats)
        cheats_stats: defaultdict[int, int] = defaultdict(int)
        for cheat in possible_cheats:
            diff: int = abs(
                original_race_stats[cheat.from_pos] - original_race_stats[cheat.to_pos]
            )
            cheat_saves: int = diff - cheat.cost
            cheats_stats[cheat_saves] += 1
        return sum(
            count if save_sec >= speedup_more_than else 0
            for save_sec, count in cheats_stats.items()
        )


def part1(input: str) -> int:
    return Map.from_input(input).count_possible_cheats(2, 2)


def part2(input: str) -> int:
    return Map.from_input(input).count_possible_cheats(100, 20)
