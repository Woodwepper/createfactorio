from dataclasses import dataclass

@dataclass
class ResourceRequirement:
    item_id: str
    amount: int

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "amount": self.amount,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ResourceRequirement":
        return cls(
            item_id=data["item_id"],
            amount=data["amount"],
        )
