from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, NamedTuple

EXPECTED_RESULT_PART1: int = 2028
EXPECTED_RESULT_PART2: int = 1751


DirectionType = Literal["^", "v", "<", ">"]


class Coords(NamedTuple):
    x: int
    y: int

    def move(self, d: Coords) -> Coords:
        return Coords(self.x + d.x, self.y + d.y)


class Direction(Coords):
    @staticmethod
    def from_string(char: DirectionType) -> Direction:
        return {
            "^": Direction(0, -1),
            "v": Direction(0, 1),
            "<": Direction(-1, 0),
            ">": Direction(1, 0),
        }[char]


@dataclass()
class Grid:
    data: list[list[str]]
    robot: Coords

    @staticmethod
    def create(input_lines: Iterable[str]) -> Grid:
        data: list[list[str]] = []
        for line in input_lines:
            if line == "\n":
                break
            data.append(list(line.strip()))

        robot: Coords | None = None

        for y in range(len(data)):
            for x in range(len(data[0])):
                if data[y][x] == "@":
                    robot = Coords(x, y)
        if not robot:
            raise ValueError("Robot 401")

        return Grid(data, robot)

    def step(self, frm: set[Coords], direction: Direction) -> None:
        next_coords: set[Coords] = {f.move(direction) for f in frm}
        for next_coord in next_coords:
            if self.data[next_coord.y][next_coord.x] == "#":
                raise ValueError("Can't move it")

        if direction in [Direction.from_string("^"), Direction.from_string("v")]:
            next_to_move: set[Coords] = set()
            for next_coord in next_coords:
                cell: str = self.data[next_coord.y][next_coord.x]
                if cell == "]":
                    next_to_move.add(Coords(next_coord.x - 1, next_coord.y))
                    next_to_move.add(next_coord)
                if cell == "[":
                    next_to_move.add(Coords(next_coord.x + 1, next_coord.y))
                    next_to_move.add(next_coord)
            if len(next_to_move) > 0:
                self.step(next_to_move, direction)

        for next_coord in next_coords:
            step_cell: str = self.data[next_coord.y][next_coord.x]
            if step_cell in "O[]":
                self.step(next_coords, direction)

        for f, next_coord in zip(sorted(frm), sorted(next_coords)):
            self.data[f.y][f.x], self.data[next_coord.y][next_coord.x] = (
                self.data[next_coord.y][next_coord.x],
                self.data[f.y][f.x],
            )

    def print(self) -> None:
        for line in self.data:
            print("".join(line))

    def simulate(self, steps: list[DirectionType]) -> None:
        for step in steps:
            direction: Direction = Direction.from_string(step)
            try:
                self.step({self.robot}, direction)
                self.robot = self.robot.move(direction)
            except ValueError:
                pass

    def count_gps(self) -> int:
        result: int = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if self.data[y][x] in "O[":
                    result += 100 * y + x
        return result

    def make_wider(self) -> None:
        new_data: list[list[str]] = []
        for y in range(len(self.data)):
            line: list[str] = []
            for x in range(len(self.data[0])):
                if self.data[y][x] == "O":
                    line += list("[]")
                if self.data[y][x] == "#":
                    line += list("##")
                if self.data[y][x] == ".":
                    line += list("..")
                if self.data[y][x] == "@":
                    line += list("@.")
            new_data.append(line)
        self.data = new_data
        self.robot = Coords(self.robot.x * 2, self.robot.y)


def get_steps(input_lines: Iterable[str]) -> list[DirectionType]:
    return [direction for line in input_lines for direction in list(line.strip())]  # type:ignore


def part1(input_lines: Iterable[str]) -> int:
    grid: Grid = Grid.create(input_lines)
    grid.simulate(get_steps(input_lines))
    return grid.count_gps()


def part2(input_lines: Iterable[str]) -> int:
    grid: Grid = Grid.create(input_lines)
    grid.make_wider()
    grid.simulate(get_steps(input_lines))
    return grid.count_gps()
