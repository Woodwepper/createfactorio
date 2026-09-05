from typing import Generic, TypeVar


DefinitionT = TypeVar("DefinitionT")


class Registry(Generic[DefinitionT]):
    """Stores definitions by their stable id."""

    def __init__(self) -> None:
        self._definitions: dict[str, DefinitionT] = {}

    def register(self, definition: DefinitionT) -> None:
        definition_id = getattr(definition, "id", None)
        if not isinstance(definition_id, str) or not definition_id:
            raise ValueError("A definition must have a non-empty string id")

        if definition_id in self._definitions:
            raise ValueError(f"Definition already registered: {definition_id}")

        self._definitions[definition_id] = definition

    def get(self, definition_id: str) -> DefinitionT | None:
        return self._definitions.get(definition_id)

    def get_all(self) -> dict[str, DefinitionT]:
        return self._definitions.copy()

    def clear(self) -> None:
        self._definitions.clear()
