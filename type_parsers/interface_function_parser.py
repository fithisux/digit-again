import dataclasses
from typing import List
import typedef_type_parser
import typedef_enum_parser
import typedef_struct_parser

type ArgType = typedef_type_parser.TypedefAlias | typedef_enum_parser.TypedefEnumAlias | typedef_struct_parser.TypedefAliasStruct | typedef_struct_parser.TypedefAliasStructPointer

type ReturnType = typedef_type_parser.TypedefAliasSimple | typedef_enum_parser.TypedefEnumAlias | typedef_struct_parser.TypedefAliasStruct | typedef_struct_parser.TypedefAliasStructPointer

@dataclasses.dataclass
class InterfaceFunction:
    function_input: List[ArgType]
    function_output: ReturnType
