from typing import List, Optional, Tuple, cast
from dspitter.domain_chunker import parser
from dspitter.code_generation.dlang import generator_transforms
from dspitter.domain_model import (
    comment_type,
    typedef_bare,
    declaration_type,
    typedef_enum,
    typedef_struct,
    typedef_union,
)


def generate(marked_parse_types: List[Tuple[bool, Optional[parser.Parse_Type]]], preample: List[str]) -> List[str]:
    generated_code: List[str] = [*preample]

    should_deprecate = False
    for deprecation_marker, parse_type in marked_parse_types:
        if not should_deprecate and deprecation_marker:
            generated_code.append("version (DUCKDB_DEPRECATED) {")
        elif should_deprecate and not deprecation_marker:
            generated_code.append("}")
        else:
            ...

        if(parse_type is None):
            generated_code.append('')
        elif(isinstance(parse_type, comment_type.CommentType)):
            generated_code.append(generator_transforms.generate_comment(cast(comment_type.CommentType, parse_type)))
        elif(isinstance(parse_type, declaration_type.DeclarationTypeFunction) or
        isinstance(parse_type, declaration_type.DeclarationTypeSimple) or 
        isinstance(parse_type, declaration_type.DeclarationSinglePointerTypeSimple) or
        isinstance(parse_type, declaration_type.DeclarationDoublePointerTypeSimple) or
        isinstance(parse_type, declaration_type.DeclarationFixedArrayTypeSimple)):
            generated_code.append(generator_transforms.generate_typedef_bare(cast(typedef_bare.TypedefBare, parse_type)))
        elif(isinstance(parse_type, declaration_type.FunctionExport)):
            generated_code.append(generator_transforms.generate_function_export(cast(declaration_type.FunctionExport, parse_type)))
        elif(isinstance(parse_type, typedef_enum.TypedefEnum)):
            generated_code.append(generator_transforms.generate_typedef_enum(cast(typedef_enum.TypedefEnum, parse_type)))
        elif(isinstance(parse_type, typedef_struct.TypedefStructValue) or isinstance(parse_type, typedef_struct.TypedefStructPointer)):
            generated_code.append(generator_transforms.generate_typedef_struct(cast(typedef_struct.TypedefStruct, parse_type)))
        elif(isinstance(parse_type, typedef_union.TypedefUnion)):
            generated_code.append(generator_transforms.generate_typedef_union(cast(typedef_union.TypedefUnion, parse_type)))

    return generated_code