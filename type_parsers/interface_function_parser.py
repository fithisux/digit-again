import dataclasses
from typing import List
import interface_type_parser
import typedef_enum_parser
import typedef_struct_parser

type ArgType = interface_type_parser.InterfaceType | typedef_enum_parser.TypedefEnumAlias | typedef_struct_parser.TypedefAliasStruct | typedef_struct_parser.TypedefAliasStructPointer

type ReturnType = interface_type_parser.InterfaceTypeSimple | typedef_enum_parser.TypedefEnumAlias | typedef_struct_parser.TypedefAliasStruct | typedef_struct_parser.TypedefAliasStructPointer


@dataclasses.dataclass
class InterfaceFunction:
    function_input: List[ArgType]
    function_name: str
    function_output: ReturnType
