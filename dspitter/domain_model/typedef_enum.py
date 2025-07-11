import dataclasses
from typing import Dict


@dataclasses.dataclass
class TypedefEnumAlias:
    enum_alias: str
    enum_label: str
    enum_fields: Dict[str, str]