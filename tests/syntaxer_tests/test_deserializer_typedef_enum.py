from syntaxer.domain_deserializer import (
    deserializer_typedef_enum,
)
from syntaxer.domain_model import (
    typedef_enum,
    exceptions,
)
from typing import cast
import pytest


def test_typedef_enum1():
    stmt = """typedef enum duckdb_state1 { 
	DuckDBSuccess = 0, 
	DuckDBError = 1 
} duckdb_state2;"""

    lines = stmt.split("\n")

    some_typedef: typedef_enum.TypedefEnum = (
        deserializer_typedef_enum.parse_typedef_enum(lines)
    )

    assert isinstance(some_typedef, typedef_enum.TypedefEnum)

    temp = cast(typedef_enum.TypedefEnum, some_typedef)
    assert temp.enum_alias == "duckdb_state2"
    assert temp.enum_label == "duckdb_state1"
    assert temp.enum_fields == {"DuckDBSuccess": "0", "DuckDBError": "1"}


def test_typedef_enum2():
    stmt = """typedef enum  { 
	DuckDBSuccess = 0, 
	DuckDBError = 1, 
} duckdb_state2;"""

    lines = stmt.split("\n")

    some_typedef: typedef_enum.TypedefEnum = (
        deserializer_typedef_enum.parse_typedef_enum(lines)
    )

    assert isinstance(some_typedef, typedef_enum.TypedefEnum)

    temp = cast(typedef_enum.TypedefEnum, some_typedef)
    assert temp.enum_alias == "duckdb_state2"
    assert temp.enum_label is None
    assert temp.enum_fields == {"DuckDBSuccess": "0", "DuckDBError": "1"}


def test_typedef_badenum():
    stmt = """typedef enum  { 
	DuckDBSuccess = 0, 
	DuckDBError = 1 
} ;"""

    lines = stmt.split("\n")
    with pytest.raises(exceptions.BadTypedefEnum):
        _ = deserializer_typedef_enum.parse_typedef_enum(lines)
