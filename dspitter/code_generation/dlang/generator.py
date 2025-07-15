from dspitter.domain_model import (
    comment_type,
    typedef_bare,
    declaration_type,
    typedef_enum,
    typedef_struct,
    typedef_union,
)
from typing import List, cast, assert_never, Tuple


def generate_comment(input: comment_type.CommentType) -> List[str]:
    if input.text == []:
        return []
    elif len(input.text) == 1:
        return ["//" + input.text[0]]
    else:
        start_comment = "/*" + input.text[0]
        end_comment = input.text[-1] + "*/"

        lines = [start_comment]
        lines.extend(input.text[1:-1])
        lines.append(end_comment)

        return lines


def generate_typedecl_plain(input: typedef_bare.TypedefBare) -> Tuple[str, str]:
    if isinstance(input, declaration_type.DeclarationTypeSimple):
        temp = cast(declaration_type.DeclarationTypeSimple, input)
        return (f"{temp.type_value}", temp.symbol_key)
    elif isinstance(input, declaration_type.DeclarationSinglePointerTypeSimple):
        temp = cast(declaration_type.DeclarationSinglePointerTypeSimple, input)
        return (f"{temp.type_value}*", temp.symbol_key)
    elif isinstance(input, declaration_type.DeclarationDoublePointerTypeSimple):
        temp = cast(declaration_type.DeclarationDoublePointerTypeSimple, input)
        return (f"{temp.type_value}**", temp.symbol_key)
    elif isinstance(input, declaration_type.DeclarationFixedArrayTypeSimple):
        temp = cast(declaration_type.DeclarationFixedArrayTypeSimple, input)
        return (f"{temp.type_value}[{temp.length}]", temp.symbol_key)
    elif isinstance(input, declaration_type.DeclarationTypeFunction):
        temp = cast(declaration_type.DeclarationTypeFunction, input)

        output_type, output_name = generate_typedecl_plain(temp.function_output)
        arg_list = ",".join(
            [
                " ".join(generate_typedecl_plain(function_input))
                for function_input in temp.function_input
            ]
        )

        return (f"{output_type} function({arg_list})", output_name)

    else:
        assert_never(input)


def generate_typedef_bare(input: typedef_bare.TypedefBare) -> str:
    if isinstance(input, declaration_type.DeclarationTypeSimple):
        temp = cast(declaration_type.DeclarationTypeSimple, input)
        return f"alias {temp.symbol_key} = {temp.type_value};"
    elif isinstance(input, declaration_type.DeclarationSinglePointerTypeSimple):
        temp = cast(declaration_type.DeclarationSinglePointerTypeSimple, input)
        return f"alias {temp.symbol_key} = {temp.type_value} *;"
    elif isinstance(input, declaration_type.DeclarationDoublePointerTypeSimple):
        temp = cast(declaration_type.DeclarationDoublePointerTypeSimple, input)
        return f"alias {temp.symbol_key} = {temp.type_value} **;"
    elif isinstance(input, declaration_type.DeclarationFixedArrayTypeSimple):
        temp = cast(declaration_type.DeclarationFixedArrayTypeSimple, input)
        return f"alias {temp.symbol_key} = {temp.type_value}[{temp.length}];"
    elif isinstance(input, declaration_type.DeclarationTypeFunction):
        temp = cast(declaration_type.DeclarationTypeFunction, input)
        output_alias = generate_typedef_bare(temp.function_output)
        inputs_list = [
            generate_typedecl_plain(function_input)
            for function_input in temp.function_input
        ]

        return f"{output_alias} function ({','.join(inputs_list)});"
    else:
        assert_never(input)


def generate_typedef_enum(input: typedef_enum.TypedefEnum) -> str:

    return f"""alias {input.enum_alias} = enum {
        ',\n'.join([enum_field[0]+' = '+enum_field[1]  for enum_field in input.enum_fields.items()])
    };"""


def generate_typedef_struct(input: typedef_struct.TypedefStruct) -> str:

    the_star = "*" if isinstance(input, typedef_struct.TypedefStructPointer) else ""
    fields_list = [
        " ".join(generate_typedecl_plain(struct_field))
        for struct_field in input.struct_declaration.struct_fields
    ]
    return f"""alias {input.struct_alias} = struct {
        ';\n'.join(fields_list)
    }{the_star};"""


def generate_typedef_union(input: typedef_union.TypedefUnion) -> str:

    fields_list = [
        " ".join(generate_typedecl_plain(union_field))
        for union_field in input.union_fields
    ]
    return f"""alias {input.union_alias} = union {
        ';\n'.join(fields_list)
    };"""


def generate_function_export(input: declaration_type.FunctionExport) -> str:

    output_type, output_name = generate_typedecl_plain(input.function_output)
    arg_list = ",".join(
        [
            " ".join(generate_typedecl_plain(function_input))
            for function_input in temp.function_input
        ]
    )

    return f"extern (C) {output_type} {output_name}({arg_list})"