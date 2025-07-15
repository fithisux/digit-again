
from typing import List
import dataclasses

class ConditionalTransitionProblem(Exception): ...


@dataclasses.dataclass
class LineTagging:
    conditional_level: int
    deprecation_conditional_level: int


def tag_lines(marker_deprecation: str, lines: List[str]) -> List[LineTagging]:
    tags: List[LineTagging] = []

    prev_tagging = LineTagging(0, 0)
    for pos, line in enumerate(lines):
        if line.lstrip(" ").startswith("#if") or line.lstrip(" ").startswith(
            "#ifndef"
        ):
            conditional_level = prev_tagging.conditional_level + 1
            deprecation_conditional_level = prev_tagging.deprecation_conditional_level
            if line.lstrip(" ").startswith(f"#ifndef {marker_deprecation}"):
                deprecation_conditional_level = deprecation_conditional_level + 1
            tags.append(LineTagging(conditional_level, deprecation_conditional_level))
        elif line.lstrip(" ").startswith("#endif"):
            conditional_level = prev_tagging.conditional_level
            deprecation_conditional_level = prev_tagging.deprecation_conditional_level
            if conditional_level == 0:
                raise ConditionalTransitionProblem()
            else:
                if conditional_level == deprecation_conditional_level:
                    deprecation_conditional_level = deprecation_conditional_level - 1

            conditional_level = conditional_level - 1
            tags.append(LineTagging(conditional_level, deprecation_conditional_level))
        else:
            tags.append(LineTagging(**dataclasses.asdict(prev_tagging)))

        print(f"Tag {tags[pos]} for line {line}")
        prev_tagging = tags[pos]
    return tags
