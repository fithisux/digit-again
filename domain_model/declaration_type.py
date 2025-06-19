import dataclasses
import typedef_type

@dataclasses.dataclass
class DeclarationTypeSimple:
    alias_key: str
    alias_value: typedef_type.InterfaceTypeSimple

type DeclarationType = DeclarationTypeSimple | typedef_type.InterfaceTypeFunction