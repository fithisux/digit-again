from syntaxer.domain_deserializer import (
    deserializer_function_export,
)
from syntaxer.domain_model import (
    declaration_type, exceptions
)
from typing import cast
import pytest


testdata = [
    "MYEXPORT void** duckdb_delete_callback_t(void *data, int ** x, doubler x);",
    "MYEXPORT void * * duckdb_delete_callback_t(void *data, int ** x, doubler x);",
    "MYEXPORT void** \n duckdb_delete_callback_t(void *data, int ** x, \n doubler x);"
]

@pytest.mark.parametrize("stmt", testdata)
def test_function_export1(stmt):
    some_typedef: declaration_type.FunctionExport = deserializer_function_export.parse_function_export('MYEXPORT', stmt.split('\n'))

    assert isinstance(some_typedef, declaration_type.FunctionExport)
    temp = cast(declaration_type.FunctionExport, some_typedef)
    assert(temp.function_output==declaration_type.DeclarationDoublePointerTypeSimple('duckdb_delete_callback_t', 'void'))
    assert(temp.function_input==[declaration_type.DeclarationSinglePointerTypeSimple('data', 'void'),
    declaration_type.DeclarationDoublePointerTypeSimple('x', 'int'),
      declaration_type.DeclarationTypeSimple('x', 'doubler'),
    ])


def test_function_export2():
    lines = [
        "MYEXPORT void** duckdb delete_callback_t(void *data, int ** x, doubler x);"
    ]

    with pytest.raises(exceptions.BadFunctionExport):
        _ = deserializer_function_export.parse_function_export('MYEXPORT', lines)