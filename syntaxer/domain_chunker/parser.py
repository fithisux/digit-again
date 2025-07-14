from typing import List, Tuple
from syntaxer.domain_chunker import chunk_reader, line_tagger
import dataclasses

class NonConformingFile(Exception): ...

@dataclasses.dataclass
class ParseConfig:
    file_name: str
    deprecation_marker: str
    function_export_marker: str


def parse_file(parse_config: ParseConfig) -> List[Tuple[bool, chunk_reader.ChunkSpec]]:

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