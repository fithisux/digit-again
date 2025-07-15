import dataclasses
from typing import List

from dspitter.domain_model import typedef_bare


@dataclasses.dataclass
class TypedefUnion:
    union_alias: str
    union_fields: List[typedef_bare.TypedefBare]
