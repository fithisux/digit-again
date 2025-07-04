from dspitter.domain_model import typedef_type, declaration_type, exceptions
import re

def parse_typedef_type(stmt : str) -> typedef_type.TypedefAlias | None:
    if("(" in stmt):
        return None
    else:
        return parse_typedef_type_simple(stmt)


def parse_typedef_type_simple(stmt : str) -> declaration_type.DeclarationTypeSimple:
    # Let's reduce spaces
    stmt = re.sub(r'\s+',' ',stmt)

    # Let's eliminate typedef

    if not stmt.startswith('typedef '):
        raise exceptions.NotATypedef()

    stmt = stmt.replace('typedef ','')

    return parse_declaration_type_simple(stmt)


def parse_declaration_type_simple(stmt : str) -> declaration_type.DeclarationTypeSimple:

    # Let's take pointers out of equation

    # Let's get them together

    stmt = re.sub(r'\* \*','**',stmt)

    # At most two stars supported

    if '***' in stmt:
        raise exceptions.MoreThanTwoStarsTypedefTypeSimple()

    # Let's tackle double stars

    if '**' in stmt:
        m = re.match(r'^(\w+)\s?\*\*\s?(\w+)$',stmt)
        if m is None:
            raise exceptions.BadDoubleStarsTypedefTypeSimple()

        return declaration_type.DeclarationTypeSimple(m.group(0), f"**{m.group(1)}")

    # Let's tackle one star

    if '*' in stmt:
        m = re.match(r'^(\w+)\s?\*\s?(\w+)$',stmt)
        if m is None:
            raise exceptions.BadSingleStarTypedefTypeSimple()
            
        return declaration_type.DeclarationTypeSimple(m.group(0), f"*{m.group(1)}")

    else:

    # No star

        m = re.match(r'^(\w+) (\w+)$',stmt)
        if m is None:
            raise exceptions.BadTypedefTypeSimple()
            
        return declaration_type.DeclarationTypeSimple(m.group(0), m.group(1))


def parse_typedef_type_function(stmt : str) -> declaration_type.DeclarationTypeSimple:
    # Let's reduce spaces
    stmt = re.sub(r'\s+',' ',stmt)

    # Let's eliminate typedef

    if not stmt.startswith('typedef '):
        raise exceptions.NotATypedefSimple()

    stmt = stmt.replace('typedef ','')

    # Let's take function out of the equation

    m = re.match(r"(\w+)\s+\(\s?\*\s?(\w+)\s?\)\s?\(([\s\,\w]*)\)", stmt)

    output_type = m.group(1)
    function_name = m.group(2)
    function_args = m.group(3)

    function_output = f"{output_type} {function_name}"

    output_type_simple = parse_declaration_type_simple(function_output)

    function_args = function_args.strip()

    if function_args == '':
        return declaration_type.DeclarationTypeFunction([], output_type_simple)

    else:
        function_inputs = function_args.split(',')
        inputs_type_simple = [parse_declaration_type_simple(function_input.strip()) for function_input in function_inputs]

        return declaration_type.DeclarationTypeFunction(inputs_type_simple, output_type_simple)

