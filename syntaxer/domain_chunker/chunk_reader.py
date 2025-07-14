from typing import List, Tuple, Optional
import dataclasses
import re
from enum import Enum, auto


class BadFunctionExportChunk(Exception): ...


class BadCCommentChunk(Exception): ...


class BadBareTypedefChunk(Exception): ...


class BadTypedefBareChunk(Exception): ...


class BadTypedefStructChunk(Exception): ...


class BadTypedefUnionChunk(Exception): ...


class BadTypedefEnumChunk(Exception): ...


# class syntax
class ChunkType(Enum):
    FUNCTION_EXPORT = auto()
    C_COMMENT = auto()
    CPP_COMMENT = auto()
    EMPTY_LINE = auto()
    TYPEDEF_BARE = auto()
    TYPEDEF_STRUCT = auto()
    TYPEDEF_UNION = auto()
    TYPEDEF_ENUM = auto()


@dataclasses.dataclass
class ChunkSpec:
    start_pos: int
    after_end_pos: int
    lines: List[str]
    chuck_type: ChunkType


def find_end_of_chunk(
    lines: List[str], lastpos: int, marker_end, some_ex: Exception
) -> int:
    target = lines[lastpos].strip().replace(" ", "")
    while not target.endswith(marker_end):
        lastpos = lastpos + 1
        if lastpos == len(lines):
            raise some_ex
        target = lines[lastpos].strip().replace(" ", "")
    return lastpos


def find_end_of_typedefchunk(lines: List[str], lastpos: int, some_ex: Exception) -> int:
    target = lines[lastpos].strip().replace(" ", "")
    m = re.match(r"}\*?\w+;$", target)
    while m is not None:
        lastpos = lastpos + 1
        if lastpos == len(lines):
            raise some_ex
        target = lines[lastpos].strip().replace(" ", "")
        m = re.match(r"}\*?\w+;$", target)
    return lastpos


def read_typedef(lines: List[str], pos: int) -> Optional[ChunkSpec]:
    lastpos = pos
    target = re.sub(r"\s+", " ", lines[pos].strip())
    if target.startswith("typedef "):
        if target.startswith("typedef struct "):
            lastpos = find_end_of_typedefchunk(lines, lastpos, BadTypedefStructChunk())
            return ChunkType(
                pos, lastpos + 1, lines[pos : (lastpos + 1)], ChunkType.TYPEDEF_STRUCT
            )
        elif target.startswith("typedef union "):
            lastpos = find_end_of_typedefchunk(lines, lastpos, BadTypedefUnionChunk())
            return ChunkType(
                pos, lastpos + 1, lines[pos : (lastpos + 1)], ChunkType.TYPEDEF_UNION
            )
        elif target.startswith("typedef enum "):
            lastpos = find_end_of_typedefchunk(lines, lastpos, BadTypedefEnumChunk())
            return ChunkType(
                pos, lastpos + 1, lines[pos : (lastpos + 1)], ChunkType.TYPEDEF_ENUM
            )
        else:
            target = re.sub(r"\s+", " ", lines[pos].strip())
            if target.endswith(";"):
                return ChunkType(
                    pos, pos + 1, lines[pos : (pos + 1)], ChunkType.TYPEDEF_STRUCT
                )
            else:
                raise BadTypedefBareChunk()
    else:
        return None


def read_function_export(
    some_marker: str, lines: List[str], pos: int
) -> Optional[ChunkSpec]:
    lastpos = pos
    target = re.sub(r"\s+", " ", lines[pos].strip())
    if target.startswith(f"{some_marker} "):
        lastpos = find_end_of_chunk(lines, lastpos, ");", BadFunctionExportChunk)
        return ChunkType(
            pos, lastpos + 1, lines[pos : (lastpos + 1)], ChunkType.FUNCTION_EXPORT
        )
    else:
        return None


def read_c_comment(lines: List[str], pos: int) -> Optional[ChunkSpec]:
    lastpos = pos
    target = re.sub(r"\s+", " ", lines[pos].strip())
    if target.startswith("/*"):
        lastpos = find_end_of_chunk(lines, lastpos, "*/", BadCCommentChunk())
        return ChunkType(
            pos, lastpos + 1, lines[pos : (lastpos + 1)], ChunkType.C_COMMENT
        )
    else:
        return None


def read_cpp_comment(lines: List[str], pos: int) -> Optional[ChunkSpec]:
    target = re.sub(r"\s+", " ", lines[pos].strip())
    if target.startswith("//"):
        return ChunkType(pos, pos + 1, lines[pos : (pos + 1)], ChunkType.CPP_COMMENT)
    else:
        return None


def read_empty_line(lines: List[str], pos: int) -> Optional[Tuple[int, str]]:
    if lines[pos].replace(" ", "") == "":
        return ChunkType(pos, pos + 1, lines[""], ChunkType.EMPTY_LINE)
    else:
        return None
