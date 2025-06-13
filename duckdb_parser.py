from typing import List, Tuple, Optional

DUCKDB_HEADER_FILE = r"C:/winoss/libduckdb-1-30-windows-amd64/duckdb_modified.h"

def preprocess_to_tags(lines: List[str]) -> List[str]:
    tags: List[str] = [None for _ in lines]
    is_in_conditional = False
    deprecation_conditional_level = 0
    conditional_level = 0
    for pos, line in enumerate(lines):
        if(line.lstrip(' ').startswith('#else')):
            if deprecation_conditional_level > 0:
                tags[pos] = f'deprecated conditional {conditional_level}'
            else:
                tags[pos] = f'conditional {conditional_level}'
        elif(line.lstrip(' ').startswith('#ifdef') or line.lstrip(' ').startswith('#ifndef')):
            conditional_level = conditional_level + 1
            is_in_conditional = True
            if(line.lstrip(' ').startswith('#ifndef DUCKDB_API_NO_DEPRECATED')):
                deprecation_conditional_level = conditional_level
            elif deprecation_conditional_level > 0:
                deprecation_conditional_level = conditional_level
            else:
                ...
            if deprecation_conditional_level > 0:
                tags[pos] = f'deprecated conditional {conditional_level}'
            else:
                tags[pos] = f'conditional {conditional_level}'
        elif(line.lstrip(' ').startswith('#endif')):
            if deprecation_conditional_level > 0:
                tags[pos] = f'deprecated conditional {conditional_level}'
            else:
                tags[pos] = f'conditional {conditional_level}'
            conditional_level = conditional_level - 1
            is_in_conditional = (conditional_level > 0)
            if deprecation_conditional_level > 0:
                deprecation_conditional_level = conditional_level
        else:
            if not is_in_conditional:
                if line.lstrip(' ').startswith('#pragma') or line.lstrip(' ').startswith('#include'):
                    tags[pos] = 'prepr'
                else:
                    tags[pos] = 'normal'
            elif deprecation_conditional_level > 0:
                tags[pos] = f'deprecated conditional {conditional_level}'
            else:
                tags[pos] = f'conditional {conditional_level}'
    return tags
            

def read_typedef(lines: List[str], pos: int) -> Optional[Tuple[int, List[str], str]]:
    lastpos = pos
    if 'typedef' in lines[pos]:
        if 'typedef struct' in lines[pos]:
            while('}' not in lines[lastpos]):
                lastpos = lastpos + 1
            return (lastpos+1, lines[pos: (lastpos+1)], 'structalias')
        elif 'typedef union' in lines[pos]:
            while('}' not in lines[lastpos]):
                lastpos = lastpos + 1
            return (lastpos+1, lines[pos: (lastpos+1)], 'unionalias')
        elif 'typedef enum' in lines[pos]:
            while('}' not in lines[lastpos]):
                lastpos = lastpos + 1
            return (lastpos+1, lines[pos: (lastpos+1)], 'enumalias')
        else:
            while(';' not in lines[lastpos]):
                lastpos = lastpos + 1
            return (lastpos+1, lines[pos: (lastpos+1)], 'typealias')
    else:
        return None

def read_function(lines: List[str], pos: int) -> Optional[Tuple[int, List[str]]]:
    lastpos = pos
    if 'DUCKDB_C_API' in lines[pos]:
        while(')' not in lines[lastpos]):
            lastpos = lastpos + 1
        return (lastpos+1, lines[pos: (lastpos+1)])
    else:
        return None

def read_c_comment(lines: List[str], pos: int) -> Optional[Tuple[int, List[str]]]:
    lastpos = pos
    if '/*' in lines[pos]:
        while('*/' not in lines[lastpos]):
            lastpos = lastpos + 1
        return (lastpos+1, lines[pos: (lastpos+1)])
    else:
        return None


def read_cpp_comment(lines: List[str], pos: int) -> Optional[Tuple[int, str]]:
    if '//' in lines[pos]:
        return (pos+1, lines[pos])
    else:
        return None


def read_empty_line(lines: List[str], pos: int) -> Optional[Tuple[int, str]]:
    if lines[pos] == '':
        return (pos+1, lines[pos])
    else:
        return None

def parse_file(file_name: str):
    deprecation_marker = False
    with open(file_name, newline='') as f:
        lines = f.read().splitlines() 
        pos = 0
        tags = preprocess_to_tags(lines)
        print(tags)
        while(pos < len(lines)):
            if tags[pos].startswith('conditional'):
                if deprecation_marker:
                    deprecation_marker = False
                pos = pos + 1
                continue
            elif tags[pos].startswith('prepr'):
                pos = pos + 1
                continue
            elif tags[pos].startswith('deprecated conditional') and not deprecation_marker:
                deprecation_marker = True
                pos = pos + 1
                continue
            elif tags[pos].startswith('deprecated conditional 1') and lines[pos].lstrip(' ').startswith('#endif'):
                deprecation_marker = False
                pos = pos + 1
                continue
            else:
                if tags[pos].startswith('normal'):
                    if deprecation_marker:
                        deprecation_marker = False

            print(f"Read line with deprecation_marker {deprecation_marker}")
            print(f"Read line with content {lines[pos]}")
            result = read_empty_line(lines, pos)
            if result is not None:
                print('read_empty_line')
                print(result[1])
                pos = result[0]
                continue
            result = read_cpp_comment(lines, pos)
            if result is not None:
                print('read_cpp_comment')
                print(result[1])
                pos = result[0]
                continue
            result = read_c_comment(lines, pos)
            if result is not None:
                print('read_c_comment')
                print(result[1])
                pos = result[0]
                continue
            result = read_function(lines, pos)
            if result is not None:
                print('read_function')
                print(result[1])
                pos = result[0]
                continue
            result = read_typedef(lines, pos)
            if result is not None:
                print(f'read_typedef {result[2]}')
                print(result[1])
                pos = result[0]
                continue
            print("We have a problem")
            break




if __name__ == "__main__":
   parse_file(DUCKDB_HEADER_FILE)