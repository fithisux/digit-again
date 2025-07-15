import dataclasses
from typing import Dict


@dataclasses.dataclass
class TypedefEnum:
    enum_alias: str
    enum_label: str
    enum_fields: Dict[str, str]
