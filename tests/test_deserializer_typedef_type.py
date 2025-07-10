from dspitter.domain_deserializer import deserializer_typedef_type
from dspitter.domain_model import typedef_type, declaration_type, exceptions
from typing import cast
import pytest

def test_typedef_simple():
    stmt = "typedef uint64_t idx_t;"

    some_typedef: typedef_type.TypedefAlias = deserializer_typedef_type.parse_typedef_type_simple(stmt)

    assert isinstance(some_typedef, declaration_type.DeclarationTypeSimple)

    temp = cast(declaration_type.DeclarationTypeSimple, some_typedef)
    assert(temp.symbol_key=='idx_t')
    assert(temp.type_value=='uint64_t')

def test_bad_typedef_simple1():
    stmt = "typedof uint64_t idx_t;"

    with pytest.raises(exceptions.NotATypedef):
        _ = deserializer_typedef_type.parse_typedef_type_simple(stmt)


def test_bad_typedef_simple2():
    stmt = "typedef idx_t;"

    with pytest.raises(exceptions.BadTypedefTypeSimple):
        _ = deserializer_typedef_type.parse_typedef_type_simple(stmt)

def test_bad_typedef_simple3():
    stmt = "typedef *  *  * idx_t;"

    with pytest.raises(exceptions.MoreThanTwoStarsTypedefTypeSimple):
        _ = deserializer_typedef_type.parse_typedef_type_simple(stmt)


testdata = [
    "typedef uint64_t *idx_t;",
    "typedef uint64_t* idx_t;",
    "typedef uint64_t *  idx_t;",
    "typedef uint64_t     *         idx_t;",
]

@pytest.mark.parametrize("stmt", testdata)
def test_typedef_singlepointer_simple(stmt):
    some_typedef: typedef_type.TypedefAlias = deserializer_typedef_type.parse_typedef_type_simple(stmt)

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
    some_typedef: typedef_type.TypedefAlias = deserializer_typedef_type.parse_typedef_type_simple(stmt)

    assert isinstance(some_typedef, declaration_type.DeclarationDoublePointerTypeSimple)
    temp = cast(declaration_type.DeclarationDoublePointerTypeSimple, some_typedef)
    assert(temp.symbol_key=='idx_t')
    assert(temp.type_value=='uint64_t')