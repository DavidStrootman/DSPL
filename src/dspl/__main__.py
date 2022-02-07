#!/usr/bin/env python3
from pprint import pprint
from pathlib import Path
import sys

from dspl.lexer import lex_file
from dspl.parser import parse

if __name__ == "__main__":
    print(f"Running on Python version {sys.version}")

    input_file_path: Path = Path("/home/david/repos/DSPL/examples/loop/loop.dspl")
    lexed_tokens = lex_file(input_file_path)
    parsed_tokens = parse(lexed_tokens)
    pprint(parsed_tokens)
