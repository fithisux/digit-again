import dataclasses
import typedef_type

@dataclasses.dataclass
class TypedefAliasSimple:
    alias_key: str
    alias_value: typedef_type.InterfaceTypeSimple

type TypedefAlias = TypedefAliasSimple | typedef_type.InterfaceTypeFunction