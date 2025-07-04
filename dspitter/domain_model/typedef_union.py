import dataclasses
from typing import Dict
from dspitter.domain_model import typedef_type

@dataclasses.dataclass
class TypedefAliasUnion:
    alias_key : str
    enum_fields: Dict[str, typedef_type.TypedefAlias]