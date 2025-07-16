from typing import List
import dataclasses


class ConditionalTransitionProblem(Exception): ...


@dataclasses.dataclass
class LineTagging:
    conditional_level: int
    is_deprecation: bool
    is_cpp: bool


def tag_lines(marker_deprecation: str, lines: List[str]) -> List[LineTagging]:
    tags: List[LineTagging] = []

    prev_tagging = LineTagging(0, False, False)
    next_is_deprecation = False
    next_is_cpp = False
    for pos, line in enumerate(lines):
        if (
            line.lstrip().startswith("#if")
            or line.lstrip().startswith("#ifdef")
            or line.lstrip().startswith("#ifndef")
        ):
            if line.lstrip().startswith(f"#ifndef {marker_deprecation}"):
                next_is_deprecation = True

            if line.lstrip().startswith("#ifdef __cplusplus"):
                next_is_cpp = True

            tags.append(LineTagging(prev_tagging.conditional_level + 1, next_is_deprecation, next_is_cpp))
        elif line.lstrip().startswith("#endif"):
            conditional_level = prev_tagging.conditional_level - 1

            if conditional_level == -1:
                raise ConditionalTransitionProblem()

            next_is_deprecation = False
            next_is_cpp = False

            tags.append(LineTagging(conditional_level, prev_tagging.is_deprecation, prev_tagging.is_cpp))
        else:
            tags.append(LineTagging(prev_tagging.conditional_level, next_is_deprecation, next_is_cpp))

        prev_tagging = tags[pos]
    return tags
