from __future__ import annotations

from abc import ABC
from copy import deepcopy
from dataclasses import dataclass

EXPECTED_RESULT_PART1: int = 1928
EXPECTED_RESULT_PART2: int = 2858


@dataclass
class MemoryBlock(ABC):
    size: int


@dataclass
class FreeBlock(MemoryBlock):
    def __repr__(self) -> str:
        return "." * self.size


@dataclass
class FileBlock(MemoryBlock):
    id: int

    def __repr__(self) -> str:
        return str(self.id) * self.size


@dataclass
class MemorySpace:
    _data: list[MemoryBlock]

    @staticmethod
    def from_line(line: str) -> MemorySpace:
        return MemorySpace(
            [
                FileBlock(id=int(idx / 2), size=int(char))
                if idx % 2 == 0
                else FreeBlock(size=int(char))
                for idx, char in enumerate(line)
            ]
        )

    def optimize(self) -> None:
        for file_block in deepcopy(self._data[::-1]):
            self._data.insert(self._data.index(file_block), FreeBlock(file_block.size))
            self._data.remove(file_block)
            if not isinstance(file_block, FileBlock):
                continue

            for free_block in self._data:
                if isinstance(free_block, FileBlock):
                    continue

                if free_block.size >= file_block.size:
                    self._data.insert(
                        self._data.index(free_block), deepcopy(file_block)
                    )
                    free_block.size -= file_block.size
                    if free_block.size == 0:
                        self._data.remove(free_block)
                    break

                self._data.insert(
                    self._data.index(free_block),
                    FileBlock(id=file_block.id, size=free_block.size),
                )
                self._data.remove(free_block)
                file_block.size -= free_block.size

    def optimize_part2(self) -> None:
        for file_block in deepcopy(self._data[::-1]):
            if not isinstance(file_block, FileBlock):
                continue

            for free_block in self._data:
                if isinstance(free_block, FileBlock):
                    if file_block.id == free_block.id:
                        break
                    continue

                if free_block.size >= file_block.size:
                    self._data.insert(
                        self._data.index(file_block), FreeBlock(file_block.size)
                    )
                    self._data.remove(file_block)
                    self._data.insert(
                        self._data.index(free_block), deepcopy(file_block)
                    )
                    if free_block.size - file_block.size == 0:
                        self._data.remove(free_block)
                    else:
                        free_block.size -= file_block.size
                    break

    def checksum(self) -> int:
        result: int = 0
        pos: int = 0
        for block in self._data:
            for _ in range(block.size):
                if isinstance(block, FileBlock):
                    result += pos * block.id
                pos += 1
        return result


"""
Really bad solution with O(inf) :D. Don't even try to understand it!
"""


def part1(line: str) -> int:
    memory_space: MemorySpace = MemorySpace.from_line(line.strip())
    memory_space.optimize()
    return memory_space.checksum()


def part2(line: str) -> int:
    memory_space: MemorySpace = MemorySpace.from_line(line.strip())
    memory_space.optimize_part2()
    return memory_space.checksum()
