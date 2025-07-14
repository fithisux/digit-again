import re
from typing import List

from syntaxer.domain_deserializer import deserializer_typedef_bare
from syntaxer.domain_model import declaration_type, exceptions


def parse_function_export(
    some_marker: str, lines: List[str]
) -> declaration_type.FunctionExport:
    # Let's reduce spaces

    stmt = "".join(lines)
    stmt = re.sub(r"\s+", " ", stmt)

    # Let's eliminate exporter

    print(f"Whole function export stmt: {stmt}")

    if not stmt.startswith(f"{some_marker} "):
        raise exceptions.NotAFunctionExport()

    stmt = stmt.replace(f"{some_marker} ", "")
    stmt = stmt.strip()

    # Let's take function out of the equation

    m = re.match(r"^(\w+[\s?\*\s?]*)\s(\w+)\s?\((.*)\)\s?;$", stmt)

    if m is None:
        print("shit!")
        raise exceptions.BadFunctionExport()

    output_type = m.group(1)
    function_name = m.group(2)
    function_args = m.group(3)

    function_output = f"typedef {output_type} {function_name};"

    output_type_simple = deserializer_typedef_bare.parse_typedef_bare_simple(
        function_output
    )

    function_args = function_args.strip()

    inputs_type_simple = []
    if function_args:
        function_inputs = function_args.split(",")
        inputs_type_simple = [
            deserializer_typedef_bare.parse_typedef_bare_simple(
                f"typedef {function_input.strip()};"
            )
            for function_input in function_inputs
        ]

    return declaration_type.FunctionExport(inputs_type_simple, output_type_simple)
