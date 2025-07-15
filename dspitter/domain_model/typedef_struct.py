import dataclasses
from typing import List, Optional

from dspitter.domain_model import typedef_bare


@dataclasses.dataclass
class StructDeclaration:
    struct_label: Optional[str]
    struct_fields: List[typedef_bare.TypedefBare]


@dataclasses.dataclass
class TypedefStructPointer:
    struct_alias: str
    struct_declaration: StructDeclaration


@dataclasses.dataclass
class TypedefStructValue:
    struct_alias: str
    struct_declaration: StructDeclaration


type TypedefStruct = TypedefStructValue | TypedefStructPointer
