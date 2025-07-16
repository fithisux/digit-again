from dspitter.domain_model import (
    comment_type,
    typedef_bare,
    declaration_type,
    typedef_enum,
    typedef_struct,
    typedef_union,
)
from typing import cast, assert_never, Tuple


def generate_comment(input: comment_type.CommentType) -> str:
    if input.text == []:
        raise ValueError("empty text in comment")
    elif len(input.text) == 1:
        return "//" + input.text[0]
    else:
        start_comment = "/*" + input.text[0]
        end_comment = input.text[-1] + "*/"

        lines = [start_comment]
        lines.extend(input.text[1:-1])
        lines.append(end_comment)

        return '\n'.join(lines)

def escape_name(type_name: Tuple[str, str]) -> Tuple[str, str]:
    return (type_name[0], f"some_{type_name[1]}" if type_name[1] in ['function', 'version', 'alias', 'set', 'out'] else type_name[1])

def typedecl_helper(input: typedef_bare.TypedefBare) -> Tuple[str, str]:
    if isinstance(input, declaration_type.DeclarationTypeSimple):
        temp = cast(declaration_type.DeclarationTypeSimple, input)
        type_value = temp.type_value
        if type_value.startswith('const '):
            type_value = f"const({type_value[6:]})"
        return (type_value, temp.symbol_key)
    elif isinstance(input, declaration_type.DeclarationSinglePointerTypeSimple):
        temp = cast(declaration_type.DeclarationSinglePointerTypeSimple, input)
        type_value = temp.type_value
        if type_value.startswith('const '):
            type_value = f"const({type_value[6:]}*)"
        else:
            type_value = f"{type_value}*"
        return (type_value, temp.symbol_key)
    elif isinstance(input, declaration_type.DeclarationDoublePointerTypeSimple):
        temp = cast(declaration_type.DeclarationDoublePointerTypeSimple, input)
        type_value = temp.type_value
        if type_value.startswith('const '):
            type_value = f"const({type_value[6:]}**)"
        else:
            type_value = f"{type_value}**"
        return (type_value, temp.symbol_key)
    elif isinstance(input, declaration_type.DeclarationFixedArrayTypeSimple):
        temp = cast(declaration_type.DeclarationFixedArrayTypeSimple, input)
        type_value = temp.type_value
        if type_value.startswith('const '):
            type_value = f"const({type_value[6:]}[{temp.length}])"
        else:
            type_value = f"{temp.type_value}[{temp.length}]"
        return (type_value, temp.symbol_key)
    elif isinstance(input, declaration_type.DeclarationTypeFunction):
        temp = cast(declaration_type.DeclarationTypeFunction, input)

        output_type, output_name = typedecl_helper(temp.function_output)
        arg_list = ",".join(
            [
                " ".join(escape_name(typedecl_helper(function_input)))
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
        return f"alias {temp.symbol_key} = {temp.type_value}*;"
    elif isinstance(input, declaration_type.DeclarationDoublePointerTypeSimple):
        temp = cast(declaration_type.DeclarationDoublePointerTypeSimple, input)
        return f"alias {temp.symbol_key} = {temp.type_value}**;"
    elif isinstance(input, declaration_type.DeclarationFixedArrayTypeSimple):
        temp = cast(declaration_type.DeclarationFixedArrayTypeSimple, input)
        return f"alias {temp.symbol_key} = {temp.type_value}[{temp.length}];"
    elif isinstance(input, declaration_type.DeclarationTypeFunction):
        temp = cast(declaration_type.DeclarationTypeFunction, input)
        output_value, output_key = typedecl_helper(temp.function_output)
        inputs_list = [
            ' '.join(typedecl_helper(function_input))
            for function_input in temp.function_input
        ]

        return f"alias {output_key} = {output_value} function({' ,'.join(inputs_list)});"
    else:
        assert_never(input)


def generate_typedef_enum(input: typedef_enum.TypedefEnum) -> str:

    return (f"enum {input.enum_alias}" + " {\n" +
        f"{',\n'.join([enum_field[0]+' = '+enum_field[1]  for enum_field in input.enum_fields.items()])}"+
        "\n};")


def generate_typedef_struct(input: typedef_struct.TypedefStruct) -> str:

    if isinstance(input, typedef_struct.TypedefStructValue):
        fields_list = [
        " ".join(typedecl_helper(struct_field))
        for struct_field in input.struct_declaration.struct_fields
    ]
        return (f"struct {input.struct_alias} " + "{\n" + f"{';\n'.join(fields_list)}"+";\n};")
    elif isinstance(input, typedef_struct.TypedefStructPointer):
        fields_list = [
        " ".join(typedecl_helper(struct_field))
        for struct_field in input.struct_declaration.struct_fields
    ]
        xxx = (f"struct {input.struct_declaration.struct_label} " + "{\n" + f"{';\n'.join(fields_list)}"+";\n};")
        xxx += f"\nalias {input.struct_alias} = {input.struct_declaration.struct_label}*;"
        return xxx


def generate_typedef_union(input: typedef_union.TypedefUnion) -> str:

    fields_list = [
        " ".join(typedecl_helper(union_field))
        for union_field in input.union_fields
    ]
    return (f"union {input.union_alias} " + "{\n" +
    f"{';\n'.join(fields_list)}"+
    ";\n};")


def generate_function_export(input: declaration_type.FunctionExport) -> str:

    output_type, output_name = typedecl_helper(input.function_output)
    arg_list = " ,".join(
        [
            ' '.join(escape_name(typedecl_helper(function_input)))
            for function_input in input.function_input
        ]
    )

    return f"extern (C) {output_type} {output_name}({arg_list});"
