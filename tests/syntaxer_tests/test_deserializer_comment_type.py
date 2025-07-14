from syntaxer.domain_deserializer import (
    deserializer_comment_type,
)
from syntaxer.domain_model import comment_type, exceptions
from typing import cast
import pytest


def test_cpp_comment():
    some_typedef: comment_type.CommentType = (
        deserializer_comment_type.parse_comment_type(["   ///   d123 ll;;;"])
    )

    assert isinstance(some_typedef, comment_type.CommentType)
    temp = cast(comment_type.CommentType, some_typedef)
    assert temp.text == ["/   d123 ll;;;"]


def test_c_comment1():
    some_typedef: comment_type.CommentType = (
        deserializer_comment_type.parse_comment_type(["   /* hehe */"])
    )

    assert isinstance(some_typedef, comment_type.CommentType)
    temp = cast(comment_type.CommentType, some_typedef)
    assert temp.text == [" hehe "]

def test_c_comment1():
    some_typedef: comment_type.CommentType = (
        deserializer_comment_type.parse_comment_type(["   /* ", "hehe */"])
    )

    assert isinstance(some_typedef, comment_type.CommentType)
    temp = cast(comment_type.CommentType, some_typedef)
    assert temp.text == [" ", "hehe "]


def test_bad_comment():
    lines = ["// ll", " abc  "]

    with pytest.raises(exceptions.NotAComment):
        _ = deserializer_comment_type.parse_comment_type(lines)
