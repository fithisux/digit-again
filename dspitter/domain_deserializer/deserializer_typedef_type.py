from dspitter.domain_model import typedef_type, declaration_type, exceptions
import re

def parse_typedef_type(stmt : str) -> typedef_type.TypedefAlias:
    if("(" in stmt):
        return parse_typedef_type_function(stmt)
    else:
        return parse_typedef_type_simple(stmt)


def parse_typedef_type_simple(stmt : str) -> declaration_type.DeclarationTypeSimple:
    # Let's reduce spaces
    stmt = re.sub(r'\s+',' ',stmt)
    stmt = stmt.strip()

    # Let's eliminate typedef

    if not stmt.startswith('typedef '):
        raise exceptions.NotATypedef()

    stmt = stmt.replace('typedef ','')

    return parse_declaration_type_simple(stmt)


def parse_declaration_type_simple(stmt : str) -> declaration_type.DeclarationTypeSimple:

    # Let's take pointers out of equation

    # Let's get them together

    stmt = re.sub(r'\*\s','*',stmt)

    # At most two stars supported

    if '***' in stmt:
        raise exceptions.MoreThanTwoStarsDeclarationPointerTypeSimple()

    # Let's tackle double stars

    print(f"Stmt is {stmt}")
    if '**' in stmt:
        
        m = re.match(r'^(\w+)\s?\*\*\s?(\w+)\s?;$',stmt)
        if m is None:
            raise exceptions.BadDeclarationDoublePointerTypeSimple()

        return declaration_type.DeclarationDoublePointerTypeSimple(m.group(2), m.group(1))

    # Let's tackle one star

    if '*' in stmt:
        m = re.match(r'^(\w+)\s?\*\s?(\w+)\s?;$',stmt)
        if m is None:
            raise exceptions.BadDeclarationSinglePointerTypeSimple()
            
        return declaration_type.DeclarationSinglePointerTypeSimple(m.group(2), m.group(1))

    else:

    # No star
        m = re.match(r'^(\w+) (\w+)\s?;$',stmt)
        if m is None:
            raise exceptions.BadDeclarationTypeSimple()
            
        return declaration_type.DeclarationTypeSimple(m.group(2), m.group(1))


def parse_typedef_type_function(stmt : str) -> declaration_type.DeclarationTypeSimple:
    # Let's reduce spaces
    stmt = re.sub(r'\s+',' ',stmt)

    # Let's eliminate typedef

    if not stmt.startswith('typedef '):
        raise exceptions.NotATypedef()

    stmt = stmt.replace('typedef ','')
    stmt = stmt.strip()

    # Let's take function out of the equation

    m = re.match(r"^(\w+[\s?\*\s?]*)\s?\(\s?\*\s?(\w+)\s?\)\s?\((.*)\)\s?;$", stmt)

    if m is None:
        raise exceptions.BadDeclarationTypeFunction()

    output_type = m.group(1)
    function_name = m.group(2)
    function_args = m.group(3)

    function_output = f"typedef {output_type} {function_name};"

    output_type_simple = parse_typedef_type_simple(function_output)

    function_args = function_args.strip()

    if function_args == '':
        return declaration_type.DeclarationTypeFunction([], output_type_simple)

    else:
        function_inputs = function_args.split(',')
        inputs_type_simple = [parse_typedef_type_simple(f"typedef {function_input.strip()};") for function_input in function_inputs]

        return declaration_type.DeclarationTypeFunction(inputs_type_simple, output_type_simple)

