from dspitter.domain_model import exceptions, typedef_enum
import re
from typing import List

def parse_typedef_enum(lines : List[str]) -> typedef_enum.TypedefEnumAlias:
    # Let's reduce spaces
    lines = [ re.sub(r'\s+',' ',line) for line in lines]
    lines = [ line.strip() for line in lines]
    lines = [ re.sub(r'\s?=\s?','=',line) for line in lines]

    # Let's eliminate typedef
    stmt = lines[0]
    if not stmt.startswith('typedef enum '):
        raise exceptions.NotATypedefEnum()

    lines[0] = stmt.replace('typedef enum ','')

    # strip c++ comments
    lines = [re.sub(r'//.*$','',line) for line in lines]

    # recover enum label
    enum_label = re.match(r'(\w+)\s?{',lines[0]).group(1)

    # recover x=y
    temp = [re.findall(r'(\w+)=(\w+)',line) for line in lines]
    equals_with_equals = []
    for some_list in temp:
        equals_with_equals.extend(some_list)

    # recover enum alias

    enum_alias = re.match(r'}\s?(\w+)\s?;', lines[-1]).group(1)

    # construct the enum

    enum_fields = {temp[0]: temp[1] for temp in equals_with_equals}
    return typedef_enum.TypedefEnumAlias(enum_alias, enum_label, enum_fields)