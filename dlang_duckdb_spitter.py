from dspitter.domain_chunker import parser
from dspitter.code_generation.dlang import generator

DUCKDB_HEADER_FILE = "modified_header_files/duckdb_modified.h"
DUCKDB_DEPRECATION_MARKER = "DUCKDB_API_NO_DEPRECATED"
DUCKDB_FUNCTION_EXPORT_MARKER = "DUCKDB_C_API"
DUCKDB_DI_FILE = "di_files/duckdb.di"

if __name__ == "__main__":
    parse_config = parser.ParseConfig(DUCKDB_HEADER_FILE, DUCKDB_DEPRECATION_MARKER, DUCKDB_FUNCTION_EXPORT_MARKER)
    chunks = parser.chunk_file(parse_config)
    parse_specs_with_deprecation = parser.parse_chunks(parse_config, chunks)
    print("All good mate")
    file_lines = generator.generate(parse_specs_with_deprecation, [])
    with open(DUCKDB_DI_FILE, 'w') as f:
        f.write('\n'.join(file_lines))
