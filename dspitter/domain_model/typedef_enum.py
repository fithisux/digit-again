import dataclasses
from typing import Dict, Optional

@dataclasses.dataclass
class EnumFieldSpec:
    enum_value: Optional[int]
    enum_comment: Optional[str]

@dataclasses.dataclass
class TypedefEnum:
    enum_name: str
    enum_fields: Dict[str, EnumFieldSpec]

@dataclasses.dataclass
class TypedefEnumAlias:
    alias_key: str
    alias_value: TypedefEnum