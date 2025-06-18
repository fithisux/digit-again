import dataclasses
from typing import Dict, Optional
import interface_type_parser

@dataclasses.dataclass
class TypedefStruct:
    struct_name: Optional[str]
    struct_fields: Dict[str, interface_type_parser.InterfaceType]

@dataclasses.dataclass
class TypedefAliasStructPointer:
    alias_key : str
    alias_value: TypedefStruct

@dataclasses.dataclass
class TypedefAliasStruct:
    alias_key : str
    alias_value: TypedefStruct