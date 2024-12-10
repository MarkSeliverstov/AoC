from pathlib import Path

from solution import EXPECTED_RESULT_PART1, EXPECTED_RESULT_PART2, part1, part2


def test():
    INPUT_EXAMPLE_PATH: Path = Path(__file__).parent / "input_example.txt"
    INPUT_PATH: Path = Path(__file__).parent / "input.txt"

    result: int = part1(open(INPUT_EXAMPLE_PATH).read().strip())
    assert result == EXPECTED_RESULT_PART1, result
    result = part1(open(INPUT_PATH).read().strip())
    print(f"Result of part 1 is {result}")

    result = part2(open(INPUT_EXAMPLE_PATH).read().strip())
    assert result == EXPECTED_RESULT_PART2, result
    result = part2(open(INPUT_PATH).read().strip())
    print(f"Result of part 2 is {result}")


if __name__ == "__main__":
    test()
