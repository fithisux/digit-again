import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class EnumField:
    enum_name: str
    enum_value: Optional[int]
    enum_comment: Optional[str]

@dataclasses.dataclass
class TypedefEnum:
    enum_name: str
    enum_fields: List[EnumField]

@dataclasses.dataclass
class TypedefEnumAlias:
    alias_key: str
    alias_value: TypedefEnum