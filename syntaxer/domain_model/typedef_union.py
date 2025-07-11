import dataclasses
from typing import List

from syntaxer.domain_model import typedef_type


@dataclasses.dataclass
class TypedefAliasUnion:
    union_alias: str
    union_fields: List[typedef_type.TypedefAlias]
