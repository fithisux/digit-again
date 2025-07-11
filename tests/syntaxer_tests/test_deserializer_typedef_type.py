from syntaxer.domain_deserializer import deserializer_typedef_type
from syntaxer.domain_model import typedef_type, declaration_type, exceptions
from typing import cast
import pytest

def test_typedef_simple():
    stmt = "typedef uint64_t idx_t;"

    some_typedef: typedef_type.TypedefAlias = deserializer_typedef_type.parse_typedef_type(stmt)

    assert isinstance(some_typedef, declaration_type.DeclarationTypeSimple)

    temp = cast(declaration_type.DeclarationTypeSimple, some_typedef)
    assert(temp.symbol_key=='idx_t')
    assert(temp.type_value=='uint64_t')

def test_bad_typedef_simple1():
    stmt = "typedof uint64_t idx_t;"

    with pytest.raises(exceptions.NotATypedef):
        _ = deserializer_typedef_type.parse_typedef_type(stmt)


def test_bad_typedef_simple2():
    stmt = "typedef idx_t;"

    with pytest.raises(exceptions.BadDeclarationTypeSimple):
        _ = deserializer_typedef_type.parse_typedef_type(stmt)

def test_bad_typedef_simple3():
    stmt = "typedef *  *  * idx_t;"

    with pytest.raises(exceptions.MoreThanTwoStarsDeclarationPointerTypeSimple):
        _ = deserializer_typedef_type.parse_typedef_type(stmt)


testdata = [
    "typedef uint64_t *idx_t;",
    "typedef uint64_t* idx_t;",
    "typedef uint64_t *  idx_t;",
    "typedef uint64_t     *         idx_t;",
]

@pytest.mark.parametrize("stmt", testdata)
def test_typedef_singlepointer_simple(stmt):
    some_typedef: typedef_type.TypedefAlias = deserializer_typedef_type.parse_typedef_type(stmt)

    assert isinstance(some_typedef, declaration_type.DeclarationSinglePointerTypeSimple)
    temp = cast(declaration_type.DeclarationTypeSimple, some_typedef)
    assert(temp.symbol_key=='idx_t')
    assert(temp.type_value=='uint64_t')


testdata = [
    "typedef uint64_t **idx_t;",
    "typedef uint64_t* *idx_t;",
    "typedef uint64_t *  *  idx_t;",
    "typedef uint64_t     * *        idx_t;",
]

@pytest.mark.parametrize("stmt", testdata)
def test_typedef_doublepointer_simple(stmt):
    some_typedef: typedef_type.TypedefAlias = deserializer_typedef_type.parse_typedef_type(stmt)

    assert isinstance(some_typedef, declaration_type.DeclarationDoublePointerTypeSimple)
    temp = cast(declaration_type.DeclarationDoublePointerTypeSimple, some_typedef)
    assert(temp.symbol_key=='idx_t')
    assert(temp.type_value=='uint64_t')


testdata = [
    "typedef void (*duckdb_delete_callback_t)(void *data);",
    "typedef void (*  duckdb_delete_callback_t)(void  * data);",
    "typedef void    (*duckdb_delete_callback_t)(void *data);",
    "typedef    void (*   duckdb_delete_callback_t )  (void * data);",
]

@pytest.mark.parametrize("stmt", testdata)
def test_typedef_function_simple1(stmt):
    some_typedef: typedef_type.TypedefAlias = deserializer_typedef_type.parse_typedef_type(stmt)

    assert isinstance(some_typedef, declaration_type.DeclarationTypeFunction)
    temp = cast(declaration_type.DeclarationTypeFunction, some_typedef)
    assert(temp.function_output==declaration_type.DeclarationTypeSimple('duckdb_delete_callback_t', 'void'))
    assert(temp.function_input==[declaration_type.DeclarationSinglePointerTypeSimple('data', 'void')])


testdata = [
    "typedef void** (*duckdb_delete_callback_t)(void *data, int ** x, doubler x);",
    "typedef void ** (*duckdb_delete_callback_t)(void *data, int ** x, doubler    x) ;",
    "typedef void** ( *duckdb_delete_callback_t)(void * data, int * * x, doubler x);",
    "typedef void* * (*duckdb_delete_callback_t)(void *data, int ** x , doubler x);",
]

@pytest.mark.parametrize("stmt", testdata)
def test_typedef_function_simple2(stmt):
    some_typedef: typedef_type.TypedefAlias = deserializer_typedef_type.parse_typedef_type(stmt)

    assert isinstance(some_typedef, declaration_type.DeclarationTypeFunction)
    temp = cast(declaration_type.DeclarationTypeFunction, some_typedef)
    assert(temp.function_output==declaration_type.DeclarationDoublePointerTypeSimple('duckdb_delete_callback_t', 'void'))
    assert(temp.function_input==[declaration_type.DeclarationSinglePointerTypeSimple('data', 'void'),
    declaration_type.DeclarationDoublePointerTypeSimple('x', 'int'),
      declaration_type.DeclarationTypeSimple('x', 'doubler'),
    ])