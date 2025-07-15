import dataclasses
from typing import List

from syntaxer.domain_model import declaration_type


@dataclasses.dataclass
class DeclarationTypeSimple:
    symbol_key: str
    type_value: str


@dataclasses.dataclass
class DeclarationSinglePointerTypeSimple:
    symbol_key: str
    type_value: str


@dataclasses.dataclass
class DeclarationDoublePointerTypeSimple:
    symbol_key: str
    type_value: str

@dataclasses.dataclass
class DeclarationFixedArrayTypeSimple:
    symbol_key: str
    type_value: str
    length: int


type DeclarationType = (
    DeclarationTypeSimple
    | DeclarationSinglePointerTypeSimple
    | DeclarationDoublePointerTypeSimple
    | DeclarationFixedArrayTypeSimple
)


@dataclasses.dataclass
class DeclarationTypeFunction:
    function_input: List[declaration_type.DeclarationType]
    function_output: declaration_type.DeclarationType


@dataclasses.dataclass
class FunctionExport:
    function_input: List[declaration_type.DeclarationType]
    function_output: declaration_type.DeclarationType
