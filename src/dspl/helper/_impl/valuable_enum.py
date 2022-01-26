from enum import Enum, unique
from typing import Tuple


@unique
class ValuableEnum(Enum):
    @classmethod
    def values(cls) -> Tuple[any, ...]:
        return tuple(value.value for value in cls.__members__.values())
