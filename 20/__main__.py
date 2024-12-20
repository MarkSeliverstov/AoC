from pathlib import Path
from time import time

from solution import EXPECTED_RESULT_PART1, EXPECTED_RESULT_PART2, part1, part2


def test():
    INPUT_EXAMPLE_PATH: Path = Path(__file__).parent / "input_example.txt"
    INPUT_PATH: Path = Path(__file__).parent / "input.txt"

    result: int = part1(open(INPUT_EXAMPLE_PATH).read())
    assert result == EXPECTED_RESULT_PART1, result
    now = time()
    result: int = part1(open(INPUT_PATH).read())
    print(f"[{time() - now:.3f} sec] Result of part 1 is {result}")

    result: int = part2(open(INPUT_EXAMPLE_PATH).read())
    assert result == EXPECTED_RESULT_PART2, result
    now = time()
    result: int = part2(open(INPUT_PATH).read())
    print(f"[{time() - now:.3f} sec] Result of part 2 is {result}")


if __name__ == "__main__":
    test()
