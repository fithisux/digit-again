import dataclasses
import interface_type_parser

@dataclasses.dataclass
class InterfaceTypeConcrete:
    referenced_type : str


@dataclasses.dataclass
class TypedefAliasSimple:
    alias_key: str
    alias_value: interface_type_parser.InterfaceTypeSimple

type TypedefAlias = TypedefAliasSimple | interface_type_parser.InterfaceTypeFunction