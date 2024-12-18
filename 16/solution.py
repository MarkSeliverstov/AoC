from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Generator, Iterable, NamedTuple

EXPECTED_RESULT_PART1: int = 11048
EXPECTED_RESULT_PART2: int = 64


class Position(NamedTuple):
    x: int
    y: int

    def distance(self, end: Position) -> int:
        return abs(self.x - end.x) ** 2 + abs(self.y - end.y) ** 2

    def step(self, distance: Position) -> Position:
        return Position(x=self.x + distance.x, y=self.y + distance.y)


DIRECTIONS: tuple[Position, ...] = (
    Position(y=-1, x=0),
    Position(y=0, x=1),
    Position(y=1, x=0),
    Position(y=0, x=-1),
)


@dataclass(frozen=True)
class Reindeer:
    position: Position
    direction: Position
    heuristic: int
    parent: Reindeer | None = None
    steps_score: int = 0

    def __repr__(self) -> str:
        return f"{self.position.y}, {self.position.x} with {self.steps_score}"

    def get_next_posibles(
        self, maze: list[list[str]], end: Position
    ) -> Generator[Reindeer]:
        new_pos: Position = self.position.step(self.direction)
        if (
            0 <= new_pos.y < len(maze)
            and 0 <= new_pos.x < len(maze[0])
            and maze[new_pos.y][new_pos.x] != "#"
        ):
            yield Reindeer(
                position=new_pos,
                direction=self.direction,
                heuristic=new_pos.distance(end),
                steps_score=self.steps_score + 1,
                parent=self,
            )

        for turn in (1, -1):
            yield Reindeer(
                position=self.position,
                direction=DIRECTIONS[(DIRECTIONS.index(self.direction) + turn) % 4],
                heuristic=new_pos.distance(end),
                steps_score=self.steps_score + 1000,
                parent=self,
            )

    @property
    def f_score(self) -> int:
        return self.steps_score + self.heuristic

    def __hash__(self) -> int:
        return hash((self.position, self.direction))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Reindeer):
            return False
        return self.position == other.position and self.direction == other.direction

    def __lt__(self, other: Reindeer) -> bool:
        return self.steps_score < other.steps_score


@dataclass()
class Maze:
    data: list[list[str]]
    start_pos: Position
    end_pos: Position

    @staticmethod
    def from_lines(input_lines: Iterable[str]) -> Maze:
        data: list[list[str]] = [list(input.strip()) for input in input_lines]
        start: Position | None = None
        end: Position | None = None
        for y in range(len(data)):
            for x in range(len(data[0])):
                if data[y][x] == "S":
                    start = Position(y=y, x=x)
                if data[y][x] == "E":
                    end = Position(y=y, x=x)
        assert start and end
        return Maze(data, start, end)

    def print(self) -> None:
        for line in self.data:
            print("".join(line))
        print()

    def find_shortest_path_a_star(self, part1: bool = True) -> int:
        queue: list[Reindeer] = []
        evaluated: dict[Reindeer, int] = {}
        best_score: int | None = None
        best_titles: set[Position] = {self.end_pos}
        heapq.heappush(
            queue,
            Reindeer(
                self.start_pos,
                DIRECTIONS[1],
                self.start_pos.distance(self.end_pos),
            ),
        )

        while queue:
            current: Reindeer = heapq.heappop(queue)
            if current in evaluated and evaluated[current] != current.steps_score:
                # So we can go on visited path if score is the same to find other shortest paths
                continue
            evaluated[current] = current.steps_score
            # for e in evaluated.keys():
            #     self.data[e.position.y][e.position.x] = "O"
            # self.print()

            if current.position == self.end_pos:
                if part1:
                    return current.steps_score

                if not best_score:
                    best_score = current.steps_score
                if best_score != current.steps_score:
                    continue

                parent = current
                while parent:
                    best_titles.add(parent.position)
                    parent = parent.parent

            for next_possible in current.get_next_posibles(self.data, self.end_pos):
                heapq.heappush(queue, next_possible)

        return best_score or -1 if part1 else len(best_titles)


def part1(input_lines: Iterable[str]) -> int:
    return Maze.from_lines(input_lines).find_shortest_path_a_star()


def part2(input_lines: Iterable[str]) -> int:
    return Maze.from_lines(input_lines).find_shortest_path_a_star(False)
