#!/usr/bin/env python3

from pathlib import Path
import sys

from lexer.lexer import lex_file

if __name__ == "__main__":
    print(f"Running on Python version {sys.version}")
    print("Hello, World!")

    input_file_path: Path = Path("/home/david/repos/DSPL/examples/loop/loop.dspl")
    [token for token in lex_file(input_file_path)]

