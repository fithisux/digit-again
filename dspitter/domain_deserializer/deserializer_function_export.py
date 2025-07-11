from dspitter.domain_model import declaration_type, exceptions
import re
from dspitter.domain_deserializer import deserializer_typedef_type
from typing import List


def parse_function_export(
    some_marker: str, lines: List[str]
) -> declaration_type.FunctionExport:
    # Let's reduce spaces

    stmt = "".join(lines)
    stmt = re.sub(r"\s+", " ", stmt)

    # Let's eliminate typedef

    if not stmt.startswith(f"{some_marker} "):
        raise exceptions.NotAFunctionExport()

    stmt = stmt.replace(f"{some_marker} ", "")

    # Let's take function out of the equation

    m = re.match(r"(\w+)\s+\(\s?\*\s?(\w+)\s?\)\s?\(([\s\,\w]*)\)", stmt)

    if m is None:
        raise exceptions.BadFunctionExport()

    output_type = m.group(1)
    function_name = m.group(2)
    function_args = m.group(3)

    function_output = f"{output_type} {function_name}"

    output_type_simple = deserializer_typedef_type.parse_declaration_type_simple(
        function_output
    )

    function_args = function_args.strip()

    inputs_type_simple = []
    if function_args:
        function_inputs = function_args.split(",")
        inputs_type_simple = [
            deserializer_typedef_type.parse_declaration_type_simple(
                function_input.strip()
            )
            for function_input in function_inputs
        ]

    return declaration_type.FunctionExport(
        inputs_type_simple, output_type_simple
    )
