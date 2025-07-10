from dspitter.domain_model import exceptions, typedef_union
from dspitter.domain_deserializer import deserializer_typedef_type
import re
from typing import List

def parse_typedef_struct(lines : List[str]) -> typedef_union.TypedefAliasUnion:
    # Let's reduce spaces
    lines = [ re.sub(r'\s+',' ',line) for line in lines]
    lines = [ line.strip() for line in lines]
    lines = [ re.sub(r'\s?=\s?','=',line) for line in lines]

    # Let's eliminate typedef
    stmt = lines[0]
    if not stmt.startswith('typedef struct '):
        raise exceptions.NotATypedefStruct()

    lines[0] = stmt.replace('typedef struct ','')

    # strip c++ comments
    lines = [re.sub(r'//.*$','',line) for line in lines]

    # recover struct fields
    union_fields = set()
    for line in lines:
        if re.match(r'\s+'):
            continue
        else:
            temp = "typedef "+line.strip()
            typedef_type = deserializer_typedef_type.parse_typedef_type(temp)
            union_fields.add(typedef_type)

    # recover struct alias
    union_alias = re.match(r'}\s?(\w+)\s?;', lines[-1]).group(1)

    # construct the struct

    return typedef_union.TypedefAliasUnion(union_alias, union_fields)