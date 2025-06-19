import dataclasses
from typing import Dict
import typedef_type

@dataclasses.dataclass
class TypedefAliasUnion:
    alias_key : str
    struct_fields: Dict[str, typedef_type.InterfaceType]