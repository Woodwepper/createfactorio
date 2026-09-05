from enum import Enum, auto

class ItemCategory(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        """Generate values as lowercase names"""
        return name.lower()

    MATERIAL = auto()
    COMPONENT = auto()
    MACHINE = auto()
    FUEL = auto()
    PRODUCT = auto()
