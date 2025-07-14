from syntaxer.domain_deserializer import (
    deserializer_typedef_struct,
)
from syntaxer.domain_model import (
    typedef_struct,
    declaration_type,
    exceptions,
)
from typing import cast
import pytest


def test_typedef_struct1():
    stmt = """typedef struct {
	int32_t year;
	int8_t month;
	int8_t day;
} duckdb_date_struct;"""

    lines = stmt.split("\n")

    some_typedef: typedef_struct.TypedefStruct = (
        deserializer_typedef_struct.parse_typedef_struct(lines)
    )

    assert isinstance(some_typedef, typedef_struct.TypedefStructValue)

    temp = cast(typedef_struct.TypedefStructValue, some_typedef)
    assert temp.struct_alias == "duckdb_date_struct"
    assert temp.struct_declaration.struct_label is None
    assert temp.struct_declaration.struct_fields == [
        declaration_type.DeclarationTypeSimple(symbol_key="year", type_value="int32_t"),
        declaration_type.DeclarationTypeSimple(symbol_key="month", type_value="int8_t"),
        declaration_type.DeclarationTypeSimple(symbol_key="day", type_value="int8_t"),
    ]


def test_typedef_struct2():
    stmt = """typedef struct duckdb_date_struct  {
	int32_t year;
	int8_t month;
	int8_t day;
} * duckdb_date_struct_t;"""

    lines = stmt.split("\n")

    some_typedef: typedef_struct.TypedefStruct = (
        deserializer_typedef_struct.parse_typedef_struct(lines)
    )

    assert isinstance(some_typedef, typedef_struct.TypedefStructPointer)

    temp = cast(typedef_struct.TypedefStructPointer, some_typedef)
    assert temp.struct_alias == "duckdb_date_struct_t"
    assert temp.struct_declaration.struct_label == "duckdb_date_struct"
    assert temp.struct_declaration.struct_fields == [
        declaration_type.DeclarationTypeSimple(symbol_key="year", type_value="int32_t"),
        declaration_type.DeclarationTypeSimple(symbol_key="month", type_value="int8_t"),
        declaration_type.DeclarationTypeSimple(symbol_key="day", type_value="int8_t"),
    ]


def test_typedef_struct3():
    stmt = """typedef struct {
	uint32_t length;
	char prefix[4];
	char *ptr;
} varchar_as_pointer;"""

    lines = stmt.split("\n")

    some_typedef: typedef_struct.TypedefStruct = (
        deserializer_typedef_struct.parse_typedef_struct(lines)
    )

    assert isinstance(some_typedef, typedef_struct.TypedefStructValue)

    temp = cast(typedef_struct.TypedefStructValue, some_typedef)
    assert temp.struct_alias == "varchar_as_pointer"
    assert temp.struct_declaration.struct_label is None
    assert temp.struct_declaration.struct_fields == [
        declaration_type.DeclarationTypeSimple(symbol_key="length", type_value="uint32_t"),
        declaration_type.DeclarationFixedArrayTypeSimple(symbol_key="prefix", type_value="char", length=4),
        declaration_type.DeclarationSinglePointerTypeSimple(symbol_key="ptr", type_value="char"),
    ]


def test_typedef_badstruct():
    stmt = """typedef struct duckdb_date_struct  {
	int32_t year;
	int8_t month;
	int8_t day;
} * ;"""

    lines = stmt.split("\n")
    with pytest.raises(exceptions.BadTypedefStruct):
        _ = deserializer_typedef_struct.parse_typedef_struct(lines)
