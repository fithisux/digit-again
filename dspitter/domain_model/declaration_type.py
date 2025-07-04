import dataclasses
from typing import List
from  dspitter.domain_model import declaration_type

@dataclasses.dataclass
class DeclarationTypeSimple:
    symbol_key: str
    type_value: str


@dataclasses.dataclass
class DeclarationTypeFunction:
    function_input: List[declaration_type.DeclarationTypeSimple]
    function_output: declaration_type.DeclarationTypeSimple


type DeclarationType = DeclarationTypeSimple | DeclarationTypeFunction