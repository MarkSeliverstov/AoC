import time
from copy import deepcopy
from dataclasses import dataclass, field
from multiprocessing import Pool, cpu_count
from typing import Iterable, Literal

EXPECTED_RESULT_PART1: int = 41
EXPECTED_RESULT_PART2: int = 6


@dataclass(frozen=True, eq=True)
class Coords:
    x: int
    y: int


DirectionType = Literal["^", "v", "<", ">"]


@dataclass(kw_only=True, eq=True, frozen=True)
class Postition:
    coords: Coords
    direction: DirectionType

    def _get_direction_one_step(self, direction: DirectionType) -> Coords:
        return {
            "^": Coords(0, -1),
            "v": Coords(0, 1),
            "<": Coords(-1, 0),
            ">": Coords(1, 0),
        }[direction]

    def get_next_step_cords(self) -> Coords:
        one_step_cords: Coords = self._get_direction_one_step(self.direction)
        return Coords(
            x=self.coords.x + one_step_cords.x,
            y=self.coords.y + one_step_cords.y,
        )

    def is_exit(self, max_y: int, max_x: int) -> bool:
        return not (0 <= self.coords.x < max_x and 0 <= self.coords.y < max_y)

    def turn_right(self) -> DirectionType:
        return {  # type:ignore
            "^": ">",
            ">": "v",
            "v": "<",
            "<": "^",
        }[self.direction]


class LoopDetected(Exception): ...


@dataclass(kw_only=True)
class Grid:
    _data: list[list[str]]
    _hight: int
    _width: int
    _guard_pos: Postition
    _visited_positions: set[Postition] = field(default_factory=set)

    @property
    def high(self) -> int:
        return self._hight

    @property
    def width(self) -> int:
        return self._width

    @staticmethod
    def from_input(input: Iterable[str]) -> "Grid":
        input_all: list[list[str]] = [list(row.strip()) for row in input if row != ""]
        grid_height: int = len(input_all)
        grid_width: int = len(input_all[0])
        for y in range(grid_height):
            for x in range(grid_width):
                if input_all[y][x] in "<>v^":
                    return Grid(
                        _data=input_all,
                        _hight=grid_height,
                        _width=grid_width,
                        _guard_pos=Postition(
                            coords=Coords(x, y),
                            direction=input_all[y][x],  # type:ignore
                        ),
                    )
        raise ValueError("Guard not found in the input grid")

    def _turn_right(self, pos: Postition) -> Postition:
        return Postition(
            coords=self._guard_pos.coords,
            direction=self._guard_pos.turn_right(),
        )

    def _step(self, pos: Postition) -> Postition:
        return Postition(
            coords=pos.get_next_step_cords(),
            direction=pos.direction,
        )

    def simulate(self) -> None:
        self._data[self._guard_pos.coords.y][self._guard_pos.coords.x] = "."
        while not self._guard_pos.is_exit(self._hight - 1, self._width - 1):
            if self._guard_pos in self._visited_positions:
                raise LoopDetected()

            if self._next_is_obstacle():
                self._guard_pos = self._turn_right(self._guard_pos)
            else:
                self._visited_positions.add(deepcopy(self._guard_pos))
                self._guard_pos = self._step(self._guard_pos)

        self._visited_positions.add(deepcopy(self._guard_pos))

    def count_visited(self) -> int:
        return len(set(pos.coords for pos in self._visited_positions))

    def _next_is_obstacle(self) -> bool:
        on_step_cords: Coords = self._guard_pos.get_next_step_cords()
        return self._data[on_step_cords.y][on_step_cords.x] == "#"


def _loop_found(grid: Grid, x: int, y: int) -> bool:
    try:
        grid_copy = deepcopy(grid)
        grid_copy._data[y][x] = "#"
        grid_copy.simulate()
    except LoopDetected:
        return True
    return False


def _bfs_possible_loop_count(
    grid: Grid, possible_obstacles_positions: set[Coords]
) -> int:
    return sum(
        1 if _loop_found(deepcopy(grid), x, y) else 0
        for x in range(grid.width)
        for y in range(grid.high)
        if (
            grid._data[y][x] not in "<>v^#"
            and Coords(x, y) in possible_obstacles_positions
        )
    )


def _multiprocessing_bfs_possible_loop_count(
    grid: Grid, possible_obstacles_positions: set[Coords]
) -> int:
    tasks: list[tuple[Grid, int, int]] = [
        (grid, x, y)
        for y in range(grid.high)
        for x in range(grid.width)
        if Coords(x, y) in possible_obstacles_positions
        and grid._data[y][x] not in "<>v^#"
    ]
    with Pool(cpu_count()) as pool:
        results = pool.starmap(_loop_found, tasks)
    return sum(results)


def part1(input_lines: Iterable[str]) -> int:
    grid: Grid = Grid.from_input(input_lines)
    grid.simulate()
    return grid.count_visited()


def part2(input_lines: Iterable[str]) -> int:
    input: list[str] = list(input_lines)
    grid = Grid.from_input(input.copy())
    grid.simulate()
    possible_obstacles_positions = {pos.coords for pos in grid._visited_positions}

    """
    It's not the best solution in terms of performance :D
    So I tried paralleling it:
        1. Wihout parallelization: 150s (_bfs_possible_loop_count)
        2. With parallelization: 14s (_multiprocessing_bfs_possible_loop_count)
    """

    # current_time: float = time.time()
    # res = _bfs_possible_loop_count(
    #     Grid.from_input(input.copy()), possible_obstacles_positions
    # )
    # print(f"Dumb BFS time: {time.time() - current_time} with {res=}")

    current_time = time.time()
    res = _multiprocessing_bfs_possible_loop_count(
        Grid.from_input(input.copy()), possible_obstacles_positions
    )
    print(f"Smart BFS time: {time.time() - current_time} with {res=}")
    return res
