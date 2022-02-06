from abc import ABC, abstractmethod


class Debuggable(ABC):
    """
    The Debuggable "mixin" marks a class as having the debug_str method, allowing other functions to print this
    information when needed.
    """
    @abstractmethod
    def debug_str(self):
        """A debug string is used for providing better error messages during both parsing and at runtime."""
