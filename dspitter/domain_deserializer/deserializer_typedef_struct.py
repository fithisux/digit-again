from dspitter.domain_model import exceptions, typedef_struct
from dspitter.domain_deserializer import deserializer_typedef_type
import re
from typing import List

def parse_typedef_struct(lines : List[str]) -> typedef_struct.TypedefStruct:
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

    # recover struct label
    struct_label = re.match(r'(\w+)\s?{',lines[0])
    if struct_label is not None:
        struct_label = struct_label.group(1)

    # recover struct fields
    struct_fields = set()
    for line in lines:
        if re.match(r'\s+'):
            continue
        else:
            temp = "typedef "+line.strip()
            typedef_type = deserializer_typedef_type.parse_typedef_type(temp)
            struct_fields.add(typedef_type)

    # recover struct alias
    alias_match = re.match(r'}\s?(\*?)?\s?(\w+)\s?;', lines[-1])
    is_pointer_alias = (alias_match.group(1) == '*')
    struct_alias = alias_match.group(2)

    # construct the struct

    if is_pointer_alias:
        return typedef_struct.TypedefAliasStructPointer(struct_alias, typedef_struct.StructDeclaration(struct_label, struct_fields))
    else:
        return typedef_struct.TypedefAliasStruct(struct_alias, typedef_struct.StructDeclaration(struct_label, struct_fields))