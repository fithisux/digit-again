import re
from typing import List
from syntaxer.domain_model import comment_type, exceptions


def parse_comment_type(lines: List[str]) -> comment_type.CommentType:
    # Let's do with one-liners

    if len(lines) == 1:
        stmt = lines[0]
        m = re.match(r"^\s+//(.*)$", stmt)
        if m is not None:
            return comment_type.CommentType([m.group(1)])

    m = re.match(r"^\s*/\*(.*)$", lines[0])

    if m is None:
        raise exceptions.NotAComment()

    for line in lines[1:]:
        if re.match(r"/\*", line):
            raise exceptions.NotAComment()

    m = re.match(r"^(.*)\*/\s*$", lines[-1])

    if m is None:
        raise exceptions.NotAComment()

    for line in lines[:-1]:
        if re.match(r"\*/", line):
            raise exceptions.NotAComment()

    # Let's eliminate exporter
    lines[0] = re.sub(r"^\s*/\*", '', lines[0])
    lines[-1] = re.sub(r"\*/\s*$", '', lines[-1])

    return comment_type.CommentType(lines)
