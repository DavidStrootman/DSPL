from enum import Enum, unique
from typing import Tuple


@unique
class ValuableEnum(Enum):
    """
    Adds functionality to Enum for retrieving all values.
    """
    @classmethod
    def values(cls) -> Tuple[any, ...]:
        """
        Retrieve all values.

        :return: returns all values of this enum (Enum.VALUE1, Enum.VALUE2, ...).
        """
        return tuple(value.value for value in cls.__members__.values())
