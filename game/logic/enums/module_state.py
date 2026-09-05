from enum import Enum, auto

class ModuleState(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        """Generate values as lowercase names"""
        return name.lower()

    NO_RECIPE = auto()
    MISSING_INPUTS = auto()
    NO_MACHINES = auto()
    NO_COMPATIBLE_MACHINES = auto()
    PRODUCING_PARTIALLY = auto()
    PRODUCING_FULLY = auto()
