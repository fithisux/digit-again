from typing import List, Tuple, Optional
from dspitter.domain_chunker import chunk_reader, line_tagger
import dataclasses

from dspitter.domain_deserializer import deserializer_comment_type, deserializer_function_export, deserializer_typedef_enum, deserializer_typedef_struct, deserializer_typedef_bare, deserializer_typedef_union
from dspitter.domain_model import comment_type, declaration_type, typedef_enum, typedef_struct, typedef_bare, typedef_union

class NonConformingFile(Exception): ...
class UnknownChunk(Exception): ...

@dataclasses.dataclass
class ParseConfig:
    file_name: str
    deprecation_marker: str
    function_export_marker: str


def chunk_file(parse_config: ParseConfig) -> List[Tuple[bool, chunk_reader.ChunkSpec]]:

    chunk_specs: List[Tuple[bool, chunk_reader.ChunkSpec]] = []
    with open(parse_config.file_name, newline="") as f:
        lines = f.read().splitlines()
        pos = 0
        tags = line_tagger.tag_lines(parse_config.deprecation_marker, lines)
        # print(tags)
        while pos < len(lines):
            print(f"Read line with deprecation_marker {tags[pos]}")
            print(f"Read line with content {lines[pos]}")

            if (tags[pos].conditional_level > 0) or (lines[pos].lstrip(' ').startswith('#')):
                pos = pos + 1
                continue

            if (result := chunk_reader.read_empty_line(lines, pos)) is not None:
                ...
            elif (result := chunk_reader.read_cpp_comment(lines, pos)) is not None:
                ...
            elif (result := chunk_reader.read_c_comment(lines, pos)) is not None:
                ...
            elif (
                result := chunk_reader.read_function_export(parse_config.function_export_marker, lines, pos)
            ) is not None:
                ...
            elif (result := chunk_reader.read_typedef(lines, pos)) is not None:
                ...
            else:
                result = None

            if result is not None:
                print(result)
                chunk_specs.append(((tags[pos].deprecation_conditional_level > 0), result))
                pos = result.after_end_pos
                continue
            else:
                raise NonConformingFile()

    return chunk_specs


type Parse_Type =  comment_type.CommentType | declaration_type.FunctionExport | typedef_enum.TypedefEnum | typedef_struct.TypedefStruct | typedef_bare.TypedefBare | typedef_union.TypedefUnion

def parse_chunks(parse_config: ParseConfig, chunks: List[Tuple[bool, chunk_reader.ChunkSpec]]) -> List[Tuple[bool, Optional[Parse_Type]]]:

    parse_specs: List[Optional[Parse_Type]] = []
    for chunk in chunks:
        print(chunk)
        match(chunk[1].chuck_type):
            case chunk_reader.ChunkType.C_COMMENT:
                parse_specs.append(deserializer_comment_type.parse_comment_type(chunk[1].lines))
            case chunk_reader.ChunkType.CPP_COMMENT:
                parse_specs.append(deserializer_comment_type.parse_comment_type(chunk[1].lines))
            case chunk_reader.ChunkType.EMPTY_LINE:
                parse_specs.append(None)
            case chunk_reader.ChunkType.FUNCTION_EXPORT:
                parse_specs.append(deserializer_function_export.parse_function_export(parse_config.function_export_marker ,chunk[1].lines))
            case chunk_reader.ChunkType.TYPEDEF_BARE:
                parse_specs.append(deserializer_typedef_bare.lines_parse_typedef_bare(chunk[1].lines))
            case chunk_reader.ChunkType.TYPEDEF_ENUM:
                parse_specs.append(deserializer_typedef_enum.parse_typedef_enum(chunk[1].lines))
            case chunk_reader.ChunkType.TYPEDEF_STRUCT:
                parse_specs.append(deserializer_typedef_struct.parse_typedef_struct(chunk[1].lines))
            case chunk_reader.ChunkType.TYPEDEF_UNION:
                parse_specs.append(deserializer_typedef_union.parse_typedef_union(chunk[1].lines))
            case _:
                raise UnknownChunk()
    
    return [(chunks[i][0], parse_specs[i]) for i,_ in enumerate(parse_specs)]