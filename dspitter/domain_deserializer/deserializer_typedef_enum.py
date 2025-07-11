import re
from typing import List

from dspitter.domain_model import exceptions, typedef_enum


def parse_typedef_enum(lines : List[str]) -> typedef_enum.TypedefEnumAlias:
    # Let's reduce spaces
    lines = [ re.sub(r'\s+',' ',line) for line in lines]
    lines = [ line.strip() for line in lines]
    lines = [ re.sub(r'\s?=\s?','=',line) for line in lines]

    # Let's eliminate typedef
    stmt = lines[0]
    if not stmt.startswith('typedef enum '):
        raise exceptions.NotATypedef()

    lines[0] = stmt.replace('typedef enum ','')

    # strip c++ comments
    lines = [re.sub(r'//.*$','',line) for line in lines]

    # make one liner
    stmt = ''.join(lines)

    print(f'Whole enum stmt: {stmt}')
    
    # recover parts of enum
    m = re.match(r'^(\w*)\s?{(.*)}\s?(\w+)\s?;$', stmt)
    if m is None:
        raise exceptions.BadTypedefEnum()

    # recover enum label
    enum_label = m.group(1)
    if enum_label == '':
        enum_label = None

    # recover enum fields
    candidate_fields = m.group(2).split(',')

    # recover x=y
    enum_fields = dict()
    for candidate_field in candidate_fields:
        m_fields = re.match(r'^(\w+)=(\w+)$',candidate_field.strip())
        if m_fields is None:
            raise exceptions.BadTypedefEnumField()
        enum_fields[m_fields.group(1)] = m_fields.group(2)

    # recover enum alias
    enum_alias = m.group(3)

    # construct the enum
    return typedef_enum.TypedefEnumAlias(enum_alias, enum_label, enum_fields)