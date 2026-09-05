from enum import Enum, auto

class FactoryState(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        """Generate values as lowercase names"""
        return name.lower()

    IDLE = auto()
    WORKING = auto()
    UNDERPOWERED = auto()
    MISSING_INPUT = auto()
    MISSING_MACHINE = auto()
    INVALID_RECIPE = auto()
