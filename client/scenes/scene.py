"""Common interface for client scenes."""

from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    """Base contract shared by menu, world, and settings scenes."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Process one Pygame event."""
        raise NotImplementedError

    @abstractmethod
    def update(self, delta_seconds: float) -> None:
        """Update the scene for one rendered frame."""
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the scene and its UI."""
        raise NotImplementedError

    @abstractmethod
    def consume_requested_action(self) -> str | None:
        """Consume the requested action and return action"""
        raise NotImplementedError
