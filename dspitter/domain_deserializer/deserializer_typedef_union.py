import re
from typing import List

from dspitter.domain_deserializer import deserializer_typedef_bare
from dspitter.domain_model import exceptions, typedef_union


def parse_typedef_union(lines: List[str]) -> typedef_union.TypedefUnion:
    # Let's reduce spaces
    lines = [re.sub(r"\s+", " ", line) for line in lines]
    lines = [line.strip() for line in lines]

    # strip c++ comments
    lines = [re.sub(r"//.*$", "", line) for line in lines]

    # Let's eliminate typedef
    stmt = "".join(lines)
    if not stmt.startswith("typedef union "):
        raise exceptions.NotATypedefUnion()

    stmt = stmt.replace("typedef union ", "")

    print(f"Whole union stmt: {stmt}")

    # recover parts of struct
    m = re.match(r"^\s?{(.*)}\s?(\w+)\s?;$", stmt)
    if m is None:
        raise exceptions.BadTypedefUnion()

    # recover union alias
    union_alias = m.group(2).strip()

    # recover union fields
    union_fields = []
    candidate_fields = m.group(1).split(";")
    if len(candidate_fields) == 1:
        raise exceptions.BadTypedefUnionField()
    candidate_fields = candidate_fields[:-1]

    for candidate_field in candidate_fields:
        temp = "typedef " + candidate_field + ";"
        typedef_bare = deserializer_typedef_bare.parse_typedef_bare(temp)
        union_fields.append(typedef_bare)

    # construct the union
    return typedef_union.TypedefUnion(union_alias, union_fields)
