import dataclasses
from typing import Set, Optional
from dspitter.domain_model import typedef_type

@dataclasses.dataclass
class TypedefStruct:
    struct_name: Optional[str]
    struct_fields: Set[str, typedef_type.TypedefAlias]

@dataclasses.dataclass
class TypedefAliasStructPointer:
    alias_key : str
    alias_value: TypedefStruct

@dataclasses.dataclass
class TypedefAliasStruct:
    alias_key : str
    alias_value: TypedefStruct