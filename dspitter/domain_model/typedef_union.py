import dataclasses
from typing import Set

from dspitter.domain_model import typedef_type


@dataclasses.dataclass
class TypedefAliasUnion:
    union_alias : str
    union_fields: Set[typedef_type.TypedefAlias]