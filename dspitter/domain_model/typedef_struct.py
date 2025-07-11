import dataclasses
from typing import List, Optional

from dspitter.domain_model import typedef_type


@dataclasses.dataclass
class StructDeclaration:
    struct_label: Optional[str]
    struct_fields: List[typedef_type.TypedefAlias]


@dataclasses.dataclass
class TypedefAliasStructPointer:
    struct_alias: str
    struct_declaration: StructDeclaration


@dataclasses.dataclass
class TypedefAliasStruct:
    struct_alias: str
    struct_declaration: StructDeclaration


type TypedefStruct = TypedefAliasStruct | TypedefAliasStructPointer
