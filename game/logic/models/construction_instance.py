from typing import Protocol


class ConstructionInstance(Protocol):
    """Runtime contract for objects that occupy a world cell."""

    cell: tuple[int, int]
