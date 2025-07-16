from dspitter.domain_model import (
    comment_type,
    declaration_type,
    typedef_enum,
    typedef_struct,
    typedef_union,
)
from dspitter.code_generation.dlang import generator_transforms
import pytest


def test_generate_comment1():
    input = comment_type.CommentType(["What you need"])
    output = generator_transforms.generate_comment(input)
    assert output == "//What you need"


def test_generate_comment2():
    input = comment_type.CommentType(["I've got ", "what you need"])
    output = generator_transforms.generate_comment(input)
    assert (
        output
        == """/*I've got 
what you need*/"""
    )


testdata = [
    (declaration_type.DeclarationTypeSimple("key", "value"), "alias key = value;"),
    (
        declaration_type.DeclarationSinglePointerTypeSimple("key", "value"),
        "alias key = value*;",
    ),
    (
        declaration_type.DeclarationDoublePointerTypeSimple("key", "value"),
        "alias key = value**;",
    ),
    (
        declaration_type.DeclarationFixedArrayTypeSimple("key", "value", 3),
        "alias key = value[3];",
    ),
    (
        declaration_type.DeclarationTypeFunction(
            [declaration_type.DeclarationDoublePointerTypeSimple("key1", "value1")],
            declaration_type.DeclarationTypeSimple("key2", "value2"),
        ),
        "alias key2 = value2 function(value1** key1);",
    ),
]


@pytest.mark.parametrize("parse_type,code_generated", testdata)
def test_generate_typedef_bare(parse_type, code_generated):
    assert generator_transforms.generate_typedef_bare(parse_type) == code_generated


def test_generate_typedef_enum():
    input = typedef_enum.TypedefEnum(
        "enum_name", None, {"key1": "value1", "key2": "value2"}
    )
    output = generator_transforms.generate_typedef_enum(input)
    assert (
        output
        == """enum enum_name {
key1 = value1,
key2 = value2
};"""
    )


def test_generate_typedef_struct1():
    input = typedef_struct.TypedefStructValue(
        "struct_name",
        typedef_struct.StructDeclaration(
            "haha",
            [
                declaration_type.DeclarationDoublePointerTypeSimple("key1", "value1"),
                declaration_type.DeclarationTypeSimple("key2", "value2"),
            ],
        ),
    )
    output = generator_transforms.generate_typedef_struct(input)
    assert (
        output
        == """struct struct_name {
value1** key1;
value2 key2;
};"""
    )


def test_generate_typedef_struct2():
    input = typedef_struct.TypedefStructPointer(
        "struct_name",
        typedef_struct.StructDeclaration(
            "haha",
            [
                declaration_type.DeclarationDoublePointerTypeSimple("key1", "value1"),
                declaration_type.DeclarationTypeSimple("key2", "value2"),
            ],
        ),
    )
    output = generator_transforms.generate_typedef_struct(input)
    assert (
        output
        == """struct haha {
value1** key1;
value2 key2;
};
alias struct_name = haha*;"""
    )


def test_generate_typedef_union():
    input = typedef_union.TypedefUnion(
        "union_name",
        [
            declaration_type.DeclarationDoublePointerTypeSimple("key1", "value1"),
            declaration_type.DeclarationTypeSimple("key2", "value2"),
        ],
    )
    output = generator_transforms.generate_typedef_union(input)
    assert (
        output
        == """union union_name {
value1** key1;
value2 key2;
};"""
    )


def test_generate_function_export1():
    input = declaration_type.DeclarationTypeFunction(
        [declaration_type.DeclarationDoublePointerTypeSimple("key1", "value1")],
        declaration_type.DeclarationTypeSimple("key2", "value2"),
    )
    output = generator_transforms.generate_function_export(input)
    assert output == "extern (C) value2 key2(value1** key1);"


def test_generate_function_export2():
    input = declaration_type.DeclarationTypeFunction(
        [], declaration_type.DeclarationTypeSimple("key2", "value2")
    )
    output = generator_transforms.generate_function_export(input)
    assert output == "extern (C) value2 key2();"
