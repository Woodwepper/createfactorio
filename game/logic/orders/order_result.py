from dataclasses import dataclass


@dataclass(frozen=True)
class OrderResult:
    order_id: str
    success: bool
    message: str
