from pathlib import Path

from solution import part1, part2


def test():
    INPUT_PATH: Path = Path(__file__).parent / "input.txt"

    result: int = part1(line for line in open(INPUT_PATH))
    print(f"Result of part 1 is {result}")

    result2: tuple[int, int] = part2(line for line in open(INPUT_PATH))
    print(f"Result of part 2 is {result2}")


if __name__ == "__main__":
    test()
