from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, NamedTuple

EXPECTED_RESULT_PART1: int = 908
EXPECTED_RESULT_PART2: int = 9021


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

    def step(self, frm: Coords, direction: Direction) -> None:
        next: Coords = frm.move(direction)
        step_cell: str = self.data[next.y][next.x]
        if step_cell == "#":
            raise ValueError("Can't move it")
        if step_cell == "O":
            self.step(next, direction)
        else:
            if step_cell == "[":
                self.step(next, direction)
                if direction in [
                    Direction.from_string("^"),
                    Direction.from_string("v"),
                ]:
                    self.step(Coords(next.x + 1, next.y), direction)
            elif step_cell == "]":
                self.step(next, direction)
                if direction in [
                    Direction.from_string("^"),
                    Direction.from_string("v"),
                ]:
                    self.step(Coords(next.x - 1, next.y), direction)

        self.data[frm.y][frm.x], self.data[next.y][next.x] = (
            self.data[next.y][next.x],
            self.data[frm.y][frm.x],
        )

    def print(self) -> None:
        for line in self.data:
            print("".join(line))

    def simulate(self, steps: list[DirectionType]) -> None:
        self.print()
        for step in steps:
            print(step)
            direction: Direction = Direction.from_string(step)
            try:
                self.step(self.robot, direction)
                self.robot = self.robot.move(direction)
            except ValueError:
                pass
            self.print()

    def count_gps(self) -> int:
        result: int = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if self.data[y][x] == "O":
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
