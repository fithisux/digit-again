import dataclasses
from typing import List
import declaration_type

@dataclasses.dataclass
class InterfaceFunction:
    function_input: List[declaration_type.DeclarationType]
    function_output: declaration_type.DeclarationTypeSimple
