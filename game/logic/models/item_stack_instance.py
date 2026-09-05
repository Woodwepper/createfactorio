from copy import deepcopy
from dataclasses import dataclass, field


@dataclass
class ItemStackInstance:
    item_id: str
    amount: int
    data: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("Item stack amount must be greater than zero.")

        self.data = deepcopy(self.data)

    def is_compatible_with(self, other: "ItemStackInstance") -> bool:
        return (
            self.item_id == other.item_id
            and self.data == other.data
        )

    def copy(self) -> "ItemStackInstance":
        return ItemStackInstance(
            item_id=self.item_id,
            amount=self.amount,
            data=deepcopy(self.data),
        )
