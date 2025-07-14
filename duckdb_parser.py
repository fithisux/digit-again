from syntaxer.domain_chunker import parser

DUCKDB_HEADER_FILE = "modified_header_files/duckdb_modified.h"
DUCKDB_DEPRECATION_MARKER = "DUCKDB_API_NO_DEPRECATED"
DUCKDB_FUNCTION_EXPORT_MARKER = "DUCKDB_C_API"


if __name__ == "__main__":
    parse_config = parser.ParseConfig(DUCKDB_HEADER_FILE, DUCKDB_DEPRECATION_MARKER, DUCKDB_FUNCTION_EXPORT_MARKER)
    _ = parser.parse_file(parse_config)
