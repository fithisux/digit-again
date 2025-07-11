from typing import List
from retriever import chunk_reader

DUCKDB_HEADER_FILE = r"modified_header_files/duckdb_modified.h"


def preprocess_to_tags(lines: List[str]) -> List[str]:
    tags: List[str] = [None for _ in lines]
    is_in_conditional = False
    deprecation_conditional_level = 0
    conditional_level = 0
    for pos, line in enumerate(lines):
        if line.lstrip(" ").startswith("#else"):
            if deprecation_conditional_level > 0:
                tags[pos] = f"deprecated conditional {conditional_level}"
            else:
                tags[pos] = f"conditional {conditional_level}"
        elif line.lstrip(" ").startswith("#ifdef") or line.lstrip(" ").startswith(
            "#ifndef"
        ):
            conditional_level = conditional_level + 1
            is_in_conditional = True
            if line.lstrip(" ").startswith("#ifndef DUCKDB_API_NO_DEPRECATED"):
                deprecation_conditional_level = conditional_level
            elif deprecation_conditional_level > 0:
                deprecation_conditional_level = conditional_level
            else:
                ...
            if deprecation_conditional_level > 0:
                tags[pos] = f"deprecated conditional {conditional_level}"
            else:
                tags[pos] = f"conditional {conditional_level}"
        elif line.lstrip(" ").startswith("#endif"):
            if deprecation_conditional_level > 0:
                tags[pos] = f"deprecated conditional {conditional_level}"
            else:
                tags[pos] = f"conditional {conditional_level}"
            conditional_level = conditional_level - 1
            is_in_conditional = conditional_level > 0
            if deprecation_conditional_level > 0:
                deprecation_conditional_level = conditional_level
        else:
            if not is_in_conditional:
                if line.lstrip(" ").startswith("#pragma") or line.lstrip(
                    " "
                ).startswith("#include"):
                    tags[pos] = "prepr"
                else:
                    tags[pos] = "normal"
            elif deprecation_conditional_level > 0:
                tags[pos] = f"deprecated conditional {conditional_level}"
            else:
                tags[pos] = f"conditional {conditional_level}"
    return tags



def parse_file(file_name: str):
    deprecation_marker = False
    with open(file_name, newline="") as f:
        lines = f.read().splitlines()
        pos = 0
        tags = preprocess_to_tags(lines)
        print(tags)
        while pos < len(lines):
            if tags[pos].startswith("conditional"):
                if deprecation_marker:
                    deprecation_marker = False
                pos = pos + 1
                continue
            elif tags[pos].startswith("prepr"):
                pos = pos + 1
                continue
            elif (
                tags[pos].startswith("deprecated conditional")
                and not deprecation_marker
            ):
                deprecation_marker = True
                pos = pos + 1
                continue
            elif tags[pos].startswith("deprecated conditional 1") and lines[pos].lstrip(
                " "
            ).startswith("#endif"):
                deprecation_marker = False
                pos = pos + 1
                continue
            else:
                if tags[pos].startswith("normal"):
                    if deprecation_marker:
                        deprecation_marker = False

            print(f"Read line with deprecation_marker {deprecation_marker}")
            print(f"Read line with content {lines[pos]}")
            result = chunk_reader.read_empty_line(lines, pos)
            if result is not None:
                print("read_empty_line")
                print(result[1])
                pos = result[0]
                continue
            result = chunk_reader.read_cpp_comment(lines, pos)
            if result is not None:
                print("read_cpp_comment")
                print(result[1])
                pos = result[0]
                continue
            result = chunk_reader.read_c_comment(lines, pos)
            if result is not None:
                print("read_c_comment")
                print(result[1])
                pos = result[0]
                continue
            result = chunk_reader.read_function_export("DUCKDB_C_API", lines, pos)
            if result is not None:
                print("read_function_export")
                print(result[1])
                pos = result[0]
                continue
            result = chunk_reader.read_typedef(lines, pos)
            if result is not None:
                print(f"read_typedef {result[2]}")
                print(result[1])
                pos = result[0]
                continue
            print("We have a problem")
            break


if __name__ == "__main__":
    parse_file(DUCKDB_HEADER_FILE)
