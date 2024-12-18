from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Generator, Iterable, NamedTuple

EXPECTED_RESULT_PART1: int = 22
EXPECTED_RESULT_PART2: int = 0


class Position(NamedTuple):
    x: int
    y: int

    def heuristic(self, end: Position) -> int:
        return abs(self.x - end.x) ** 2 + abs(self.y - end.y) ** 2


@dataclass(frozen=True)
class Historian:
    position: Position
    heuristic: int
    # path: set[Position] = field(default_factory=set)
    steps_score: int = 0

    def __repr__(self) -> str:
        return f"{self.position.y}, {self.position.x} with {self.steps_score}"

    def get_next_posibles(
        self, maze: list[list[str]], end: Position
    ) -> Generator[Historian]:
        for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            new_pos: Position = Position(y=self.position.y + dy, x=self.position.x + dx)
            if (
                0 <= new_pos.y < len(maze)
                and 0 <= new_pos.x < len(maze[0])
                and maze[new_pos.y][new_pos.x] != "#"
            ):
                yield Historian(
                    position=new_pos,
                    heuristic=new_pos.heuristic(end),
                    steps_score=self.steps_score + 1,
                    # path=deepcopy(self.path) | {self.position},
                )

    @property
    def f_score(self) -> int:
        return self.steps_score + self.heuristic

    def __hash__(self) -> int:
        return hash(self.position)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Historian):
            return False
        return self.position == other.position

    def __lt__(self, other: Historian) -> bool:
        return self.steps_score < other.steps_score


@dataclass()
class MemorySpace:
    data: list[list[str]]
    other_bytes: list[Position]

    @staticmethod
    def from_input(
        lines: Iterable[str], width: int = 6, high: int = 6, bytes_remain: int = 12
    ) -> MemorySpace:
        data: list[list[str]] = [
            ["." for _ in range(width + 1)] for _ in range(high + 1)
        ]
        other_bytes: list[Position] = []
        for line in lines:
            x, y = line.strip().split(",")
            if bytes_remain == 0:
                other_bytes.append(Position(y=int(y), x=int(x)))
            else:
                data[int(y)][int(x)] = "#"
                bytes_remain -= 1
        return MemorySpace(data, other_bytes)

    def print(self) -> None:
        for line in self.data:
            print("".join(line))
        print()

    def find_shortest_path_a_star(self) -> int:
        queue: list[Historian] = []
        evaluated: set[Historian] = set()
        start_pos: Position = Position(0, 0)
        end_pos: Position = Position(y=len(self.data) - 1, x=len(self.data[0]) - 1)
        heapq.heappush(queue, Historian(start_pos, start_pos.heuristic(end_pos)))

        while queue:
            current: Historian = heapq.heappop(queue)
            if current.position == end_pos:
                # for p in current.path:
                #     self.data[p.y][p.x] = "O"
                # self.print()
                return current.steps_score

            if current in evaluated:
                continue
            evaluated.add(current)

            for next_possible in current.get_next_posibles(self.data, end_pos):
                heapq.heappush(queue, next_possible)

        raise Exception("End pos not found")

    def find_first_possible_block(self) -> tuple[int, int]:
        for x, y in self.other_bytes:
            self.data[y][x] = "#"
            # print(x, y)
            try:
                self.find_shortest_path_a_star()
            except:
                # self.print()
                return x, y
        return 0, 0


def part1(input_lines: Iterable[str]) -> int:
    return MemorySpace.from_input(input_lines, 70, 70, 1024).find_shortest_path_a_star()


def part2(input_lines: Iterable[str]) -> tuple[int, int]:
    return MemorySpace.from_input(input_lines, 70, 70, 1024).find_first_possible_block()
