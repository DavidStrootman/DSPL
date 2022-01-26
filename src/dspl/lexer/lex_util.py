from dataclasses import dataclass
from typing import TextIO


@dataclass
class DebugData:
    """Holds data used during exception handling for debugging purposes."""
    line: int
    start_pos: int = None

    def __str__(self) -> str:
        return f"{self.line + 1}"


@dataclass
class Word:
    """
    Wrapper for a literal word holding the original lexed word and debug data.
    Words are either a sequence of letters, or a single symbol.
    """
    debug_data: DebugData
    content: str

