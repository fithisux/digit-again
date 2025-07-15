import dataclasses
from typing import List


@dataclasses.dataclass
class CommentType:
    text: List[str]