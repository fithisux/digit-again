from dspitter.domain_deserializer import (
    deserializer_typedef_type,
    deserializer_typedef_struct,
)
from dspitter.domain_model import (
    typedef_type,
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

    assert isinstance(some_typedef, typedef_struct.TypedefAliasStruct)

    temp = cast(typedef_struct.TypedefAliasStruct, some_typedef)
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

    assert isinstance(some_typedef, typedef_struct.TypedefAliasStructPointer)

    temp = cast(typedef_struct.TypedefAliasStructPointer, some_typedef)
    assert temp.struct_alias == "duckdb_date_struct_t"
    assert temp.struct_declaration.struct_label == "duckdb_date_struct"
    assert temp.struct_declaration.struct_fields == [
        declaration_type.DeclarationTypeSimple(symbol_key="year", type_value="int32_t"),
        declaration_type.DeclarationTypeSimple(symbol_key="month", type_value="int8_t"),
        declaration_type.DeclarationTypeSimple(symbol_key="day", type_value="int8_t"),
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
