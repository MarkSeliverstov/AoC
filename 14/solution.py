from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Iterable

EXPECTED_RESULT_PART1: int = 21

TILES_WIDE: int = 101
TILES_TALL: int = 103
SIMULATION_TIME_SEC: int = 100


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class Robot:
    pos: Position
    vx: int
    vy: int

    @staticmethod
    def from_values(x, y, vx, vy) -> Robot:
        return Robot(Position(x, y), vx, vy)

    def get_simulated_pos(self, sec: int, wide: int, tall: int) -> Position:
        return Position(
            (self.vx * sec + self.pos.x) % wide, (self.vy * sec + self.pos.y) % tall
        )


def get_robots_in_quadrats(position: list[Position], wide: int, tall: int) -> int:
    robots_in_quadrats: list[int] = [0, 0, 0, 0]
    for robot in position:
        if robot.x < wide // 2:
            if robot.y < tall // 2:
                robots_in_quadrats[0] += 1
            elif robot.y > tall // 2:
                robots_in_quadrats[2] += 1
        elif robot.x > wide // 2:
            if robot.y < tall // 2:
                robots_in_quadrats[1] += 1
            elif robot.y > tall // 2:
                robots_in_quadrats[3] += 1
    return math.prod(robots_in_quadrats)


def part1(input_lines: Iterable[str]) -> int:
    robots: list[Robot] = [
        Robot.from_values(*[int(value) for value in re.findall(r"[-]?\d+", line)])
        for line in input_lines
    ]
    simulated_positions: list[Position] = [
        robot.get_simulated_pos(SIMULATION_TIME_SEC, TILES_WIDE, TILES_TALL)
        for robot in robots
    ]
    return get_robots_in_quadrats(simulated_positions, TILES_WIDE, TILES_TALL)


def part2(input_lines: Iterable[str]) -> int:
    robots: list[Robot] = [
        Robot.from_values(*[int(value) for value in re.findall(r"[-]?\d+", line)])
        for line in input_lines
    ]
    for seconds in range(1, TILES_TALL * TILES_WIDE * 2):
        positions: list[Position] = [
            robot.get_simulated_pos(seconds, TILES_WIDE, TILES_TALL)
            for robot in robots
        ]
        grid: list[list[str]] = [
            ["." for _ in range(TILES_WIDE)] for _ in range(TILES_TALL)
        ]
        for position in positions:
            grid[position.y][position.x] = "#"

        for line in grid:
            if re.match(r".*#########.*", "".join(line)):
                for linee in grid:
                    print("".join(linee))
                return seconds
    return 0
