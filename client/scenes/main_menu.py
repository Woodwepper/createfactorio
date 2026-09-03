"""Main menu scene."""

import pygame
import pygame_gui

from client.config import BACKGROUND_COLOR, WINDOW_SIZE
from client.scenes.scene import Scene


class MainMenuScene(Scene):
    """Initial scene shown before a World is created."""

    BUTTON_SIZE = (240, 60)
    BUTTON_GAP = 16

    def __init__(self) -> None:
        self.ui_manager = pygame_gui.UIManager(WINDOW_SIZE)
        self.requested_action: str | None = None

        self.create_world_button = self._create_button("Create world", 0)
        self.settings_button = self._create_button("Settings", 1)
        self.exit_button = self._create_button("Exit", 2)

    def _create_button(self, text: str, index: int) -> pygame_gui.elements.UIButton:
        button_width, button_height = self.BUTTON_SIZE
        total_height = (button_height * 3) + (self.BUTTON_GAP * 2)
        first_y = (WINDOW_SIZE[1] - total_height) // 2
        button_y = first_y + index * (button_height + self.BUTTON_GAP)

        rect = pygame.Rect(
            (WINDOW_SIZE[0] - button_width) // 2,
            button_y,
            button_width,
            button_height,
        )

        return pygame_gui.elements.UIButton(
            relative_rect=rect,
            text=text,
            manager=self.ui_manager,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        self.ui_manager.process_events(event)

        if event.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        if event.ui_element == self.create_world_button:
            self.requested_action = "create_world"
        elif event.ui_element == self.settings_button:
            self.requested_action = "settings"
        elif event.ui_element == self.exit_button:
            self.requested_action = "exit"

    def consume_requested_action(self) -> str | None:
        action = self.requested_action
        self.requested_action = None
        return action

    def update(self, delta_seconds: float) -> None:
        self.ui_manager.update(delta_seconds)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        self.ui_manager.draw_ui(screen)
