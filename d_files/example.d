import duckdb;
import std.stdio;

void main() {

    writeln("12345");
    duckdb_database db = null;
    duckdb_connection con = null;
    duckdb_result result;

    scope(exit) {
        duckdb_destroy_result(&result);
        duckdb_disconnect(&con);
        duckdb_close(&db);
    }

    if (duckdb_open(null, &db) == duckdb_state.DuckDBError) {
        writeln("Failed to open database\n");
        writeln("1\n");
        return;
    }
    if (duckdb_connect(db, &con) == duckdb_state.DuckDBError) {
        writeln("Failed to open connection\n");
        writeln("2\n");
        return;
    }
    if (duckdb_query(con, "CREATE TABLE integers(i INTEGER, j INTEGER);", null) == duckdb_state.DuckDBError) {
        writeln("Failed to query database\n");
        writeln("3\n");
        return;
    }
    if (duckdb_query(con, "INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL);", null) == duckdb_state.DuckDBError) {
        writeln("Failed to query database\n");
        writeln("4\n");
        return;
    }
    if (duckdb_query(con, "SELECT * FROM integers", &result) == duckdb_state.DuckDBError) {
        writeln("Failed to query database\n");
        writeln("5\n");
        return;
    }
    // print the names of the result
    idx_t row_count = duckdb_row_count(&result);
    idx_t column_count = duckdb_column_count(&result);
    for (size_t i = 0; i < column_count; i++) {
        writeln("column name");
        writeln(duckdb_column_name(&result, i));
    }
    printf("\n");
    // print the data of the result
    for (size_t row_idx = 0; row_idx < row_count; row_idx++) {
        for (size_t col_idx = 0; col_idx < column_count; col_idx++) {
            char *val = duckdb_value_varchar(&result, col_idx, row_idx);
            writeln("value for row_idx ", row_idx, " col idx ", col_idx);
            writeln(val);
            duckdb_free(val);
        }
        writeln("\n");
    }
    // duckdb_print_result(result);
}