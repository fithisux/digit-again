import dataclasses
from typing import Dict, Optional


@dataclasses.dataclass
class TypedefEnum:
    enum_alias: str
    enum_label: Optional[str]
    enum_fields: Dict[str, str]
