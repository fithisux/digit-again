import dataclasses
from typing import List

from dspitter.domain_model import declaration_type


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


type DeclarationType = (
    DeclarationTypeSimple
    | DeclarationSinglePointerTypeSimple
    | DeclarationDoublePointerTypeSimple
)


@dataclasses.dataclass
class DeclarationTypeFunction:
    function_input: List[declaration_type.DeclarationType]
    function_output: declaration_type.DeclarationType


@dataclasses.dataclass
class FunctionExport:
    function_input: List[declaration_type.DeclarationType]
    function_output: declaration_type.DeclarationType
