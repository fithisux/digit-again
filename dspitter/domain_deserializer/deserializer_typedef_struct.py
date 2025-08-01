import re
from typing import List

from dspitter.domain_deserializer import deserializer_typedef_bare
from dspitter.domain_model import exceptions, typedef_struct


def parse_typedef_struct(lines: List[str]) -> typedef_struct.TypedefStruct:
    # Let's reduce spaces
    lines = [re.sub(r"\s+", " ", line) for line in lines]
    lines = [line.strip() for line in lines]

    # strip c++ comments
    lines = [re.sub(r"//.*$", "", line) for line in lines]

    # Let's eliminate typedef
    stmt = "".join(lines)
    if not stmt.startswith("typedef struct "):
        raise exceptions.NotATypedefStruct()

    stmt = stmt.replace("typedef struct ", "")

    # recover parts of struct
    m = re.match(r"^(\w*)\s?{(.*)}\s?(\*?\s?\w+)\s?;$", stmt)
    if m is None:
        raise exceptions.BadTypedefStruct()

    # recover struct label
    struct_label = m.group(1)
    if struct_label == "":
        struct_label = None

    # recover struct alias
    struct_alias = m.group(3).strip()
    is_pointer_alias = struct_alias.startswith("*")
    struct_alias = struct_alias.replace("*", "")
    struct_alias = struct_alias.replace(" ", "")

    # last entry may end up with ;
    candidate_fields = m.group(2).split(";")
    if re.match(r'^\s*$', candidate_fields[-1]):
        candidate_fields = candidate_fields[:-1]
        if len(candidate_fields) == 0:
            raise exceptions.BadTypedefStructField()

    # recover struct fields
    struct_fields = []
    for candidate_field in candidate_fields:
        temp = "typedef " + candidate_field + ";"
        typedef_bare = deserializer_typedef_bare.parse_typedef_bare(temp)
        struct_fields.append(typedef_bare)

    # construct the struct

    if is_pointer_alias:
        return typedef_struct.TypedefStructPointer(
            struct_alias, typedef_struct.StructDeclaration(struct_label, struct_fields)
        )
    else:
        return typedef_struct.TypedefStructValue(
            struct_alias, typedef_struct.StructDeclaration(struct_label, struct_fields)
        )
