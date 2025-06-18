import dataclasses
from typing import List

@dataclasses.dataclass
class InterfaceTypeConcrete:
    referenced_type : str

@dataclasses.dataclass
class InterfaceTypePointer:
    nonreferenced_type : str


type InterfaceTypeSimple = InterfaceTypeConcrete | InterfaceTypePointer

@dataclasses.dataclass
class InterfaceTypeFunction:
    function_input: List[InterfaceTypeSimple]
    function_name: str
    function_output: InterfaceTypeSimple

type InterfaceType = InterfaceTypeSimple | InterfaceTypeFunction