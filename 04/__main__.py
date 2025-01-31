from pathlib import Path

from solution import EXPECTED_RESULT_PART1, EXPECTED_RESULT_PART2, part1, part2


def test():
    INPUT_EXAMPLE_PATH: Path = Path(__file__).parent / "input_example.txt"
    INPUT_EXAMPLE_2_PATH: Path = Path(__file__).parent / "input_example_2.txt"
    INPUT_PATH: Path = Path(__file__).parent / "input.txt"

    result: int = part1(line for line in open(INPUT_EXAMPLE_PATH))
    assert result == EXPECTED_RESULT_PART1, result
    result: int = part1(line for line in open(INPUT_PATH))
    print(f"Result of part 1 is {result}")

    result: int = part2(line for line in open(INPUT_EXAMPLE_2_PATH))
    assert result == EXPECTED_RESULT_PART2, result
    result: int = part2(line for line in open(INPUT_PATH))
    print(f"Result of part 2 is {result}")


if __name__ == "__main__":
    test()
