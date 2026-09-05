from dataclasses import dataclass, field
import uuid

from game.logic.enums.construction_type import ConstructionType


@dataclass(frozen=True)
class PlaceConstructionOrder:
    construction_type: ConstructionType
    definition_id: str
    cell: tuple[int, int]
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))
