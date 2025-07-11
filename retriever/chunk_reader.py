from typing import List, Tuple, Optional

def read_typedef(lines: List[str], pos: int) -> Optional[Tuple[int, List[str], str]]:
    lastpos = pos
    if "typedef" in lines[pos]:
        if "typedef struct" in lines[pos]:
            while "}" not in lines[lastpos]:
                lastpos = lastpos + 1
            return (lastpos + 1, lines[pos : (lastpos + 1)], "structalias")
        elif "typedef union" in lines[pos]:
            while "}" not in lines[lastpos]:
                lastpos = lastpos + 1
            return (lastpos + 1, lines[pos : (lastpos + 1)], "unionalias")
        elif "typedef enum" in lines[pos]:
            while "}" not in lines[lastpos]:
                lastpos = lastpos + 1
            return (lastpos + 1, lines[pos : (lastpos + 1)], "enumalias")
        else:
            while ";" not in lines[lastpos]:
                lastpos = lastpos + 1
            return (lastpos + 1, lines[pos : (lastpos + 1)], "typealias")
    else:
        return None


def read_function_export(some_marker: str, lines: List[str], pos: int) -> Optional[Tuple[int, List[str]]]:
    lastpos = pos
    if some_marker in lines[pos]:
        while ")" not in lines[lastpos]:
            lastpos = lastpos + 1
        return (lastpos + 1, lines[pos : (lastpos + 1)])
    else:
        return None


def read_c_comment(lines: List[str], pos: int) -> Optional[Tuple[int, List[str]]]:
    lastpos = pos
    if "/*" in lines[pos]:
        while "*/" not in lines[lastpos]:
            lastpos = lastpos + 1
        return (lastpos + 1, lines[pos : (lastpos + 1)])
    else:
        return None


def read_cpp_comment(lines: List[str], pos: int) -> Optional[Tuple[int, str]]:
    if "//" in lines[pos]:
        return (pos + 1, lines[pos])
    else:
        return None


def read_empty_line(lines: List[str], pos: int) -> Optional[Tuple[int, str]]:
    if lines[pos] == "":
        return (pos + 1, lines[pos])
    else:
        return None

