import dataclasses
from typing import Dict, Optional
import typedef_type

@dataclasses.dataclass
class TypedefStruct:
    struct_name: Optional[str]
    struct_fields: Dict[str, typedef_type.InterfaceType]

@dataclasses.dataclass
class TypedefAliasStructPointer:
    alias_key : str
    alias_value: TypedefStruct

@dataclasses.dataclass
class TypedefAliasStruct:
    alias_key : str
    alias_value: TypedefStruct