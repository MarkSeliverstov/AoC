from typing import DefaultDict, Iterable

EXPECTED_RESULT_PART1: int = 143
EXPECTED_RESULT_PART2: int = 123


def _get_smarter_rules(input_lines: Iterable[str]) -> dict[int, set[int]]:
    """
    Returns a dictionary where the values represent the numbers
    that are not allowed to be on the right of the key, e.g. must be on the left.
    """

    result: DefaultDict[int, set[int]] = DefaultDict(set)
    for line in input_lines:
        if line == "\n":
            return result

        left, right = line.strip().split("|")
        result[int(right)].add(int(left))
    return result


def _is_safe_ordering(ordering: list[int], rules: dict[int, set[int]]) -> bool:
    return all(
        (right_num not in rules[ordering[current_num_idx]])
        for current_num_idx in range(len(ordering))
        for right_num in ordering[current_num_idx + 1 :]
    )


def _fix_ordering(ordering: list[int], rules: dict[int, set[int]]) -> list[int]:
    """Go through the ordering and swap the numbers that are not in the correct order"""

    for curr_num_idx in range(len(ordering)):
        for right_num_idx in range(curr_num_idx + 1, len(ordering)):
            if ordering[right_num_idx] in rules[ordering[curr_num_idx]]:
                ordering[curr_num_idx], ordering[right_num_idx] = (
                    ordering[right_num_idx],
                    ordering[curr_num_idx],
                )
    return ordering


def part1(input_lines: Iterable[str]) -> int:
    smart_rules: dict[int, set[int]] = _get_smarter_rules(input_lines)
    result: int = 0
    for line in input_lines:
        ordering: list[int] = [int(element) for element in line.split(",")]
        if _is_safe_ordering(ordering, smart_rules):
            result += ordering[int(len(ordering) / 2)]
    return result


def part2(input_lines: Iterable[str]) -> int:
    smart_rules: dict[int, set[int]] = _get_smarter_rules(input_lines)
    result: int = 0
    for line in input_lines:
        ordering: list[int] = [int(element) for element in line.split(",")]
        if not _is_safe_ordering(ordering, smart_rules):
            ordering = _fix_ordering(ordering, smart_rules)
            result += ordering[int(len(ordering) / 2)]
    return result
