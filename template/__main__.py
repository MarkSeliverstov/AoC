import sys
from collections.abc import Iterator

from solution import first_part_solution, second_part_solution


def read_file_generator(file_name: str = "input.txt") -> Iterator[str]:
    with open(file_name) as file:
        for line in file:
            yield line


def test_simple_input_data_generator() -> Iterator[str]:
    input: str = """"""
    for row in input.splitlines():
        yield row


USAGE_MESSAGE: str = (
    "Usage:\t python <dir> - to get results from input.txt\n"
    + "\t python <dir> test <first_result> <second_result> - to test script"
    + "\nExample: python 1 test 11 35"
)


def start():
    if len(sys.argv) == 1:
        first_result = first_part_solution(read_file_generator())
        print(f"{first_result=}")
        second_result = second_part_solution(read_file_generator())
        print(f"{second_result=}")
        return

    if sys.argv[1] == "test":
        if len(sys.argv) < 3:
            print(USAGE_MESSAGE)
            return

        if len(sys.argv) >= 3:
            first_expected_result: int = int(sys.argv[2])
            first_result: int = first_part_solution(test_simple_input_data_generator())
            assert first_result == first_expected_result, first_result
            print(f"First part test passed: {first_result=}")

        if len(sys.argv) == 4:
            second_expected_result: int = int(sys.argv[3])
            second_result: int = second_part_solution(
                test_simple_input_data_generator()
            )
            assert second_result == second_expected_result, second_result
            print(f"Second part test passed: {second_result=}")
    else:
        print(USAGE_MESSAGE)


if __name__ == "__main__":
    start()
