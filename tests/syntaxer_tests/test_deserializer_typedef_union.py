from syntaxer.domain_deserializer import (
    deserializer_typedef_union,
)
from syntaxer.domain_model import (
    typedef_union,
    declaration_type,
    exceptions,
)
from typing import cast
import pytest


def test_typedef_union():
    stmt = """typedef union {
	int32_t year;
	int8_t *month;
	int8_t(*day)(road **trip);
} duckdb_date;"""

    lines = stmt.split("\n")

    some_typedef: typedef_union.TypedefUnion = (
        deserializer_typedef_union.parse_typedef_union(lines)
    )

    assert isinstance(some_typedef, typedef_union.TypedefUnion)

    temp = cast(typedef_union.TypedefUnion, some_typedef)
    assert temp.union_alias == "duckdb_date"
    assert temp.union_fields[0] == declaration_type.DeclarationTypeSimple(
        symbol_key="year", type_value="int32_t"
    )
    assert temp.union_fields[1] == declaration_type.DeclarationSinglePointerTypeSimple(
        symbol_key="month", type_value="int8_t"
    )
    assert temp.union_fields[2] == declaration_type.DeclarationTypeFunction(
        [declaration_type.DeclarationDoublePointerTypeSimple("trip", "road")],
        declaration_type.DeclarationTypeSimple(symbol_key="day", type_value="int8_t")
    )


def test_typedef_badunion():
    stmt = """typedef union {
	int32_t year;
	int8_t **month;
	int8_t(*day)(road **trip);
} ;"""

    lines = stmt.split("\n")
    with pytest.raises(exceptions.BadTypedefUnion):
        _ = deserializer_typedef_union.parse_typedef_union(lines)
