import pygame
import pygame_gui

from game.logic.content.game_definitions import ConstructionOption


class ConstructionMenu:
    PANEL_POSITION = (15, 200)
    PANEL_WIDTH = 200

    BUTTON_SIZE = (170, 50)
    BUTTON_GAP = 10
    BUTTON_MARGIN = 10

    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        options: list[ConstructionOption],
    ) -> None:
        self.ui_manager = ui_manager
        self.options = options
        self.selected_construction: ConstructionOption | None = None
        self.buttons: dict[
            pygame_gui.elements.UIButton,
            ConstructionOption,
        ] = {}

        button_count = len(options) + 1  # construction options + Cancel
        panel_height = (
            (button_count * self.BUTTON_SIZE[1])
            + ((button_count - 1) * self.BUTTON_GAP)
            + (2 * self.BUTTON_MARGIN)
        )
        panel_rect = pygame.Rect(
            self.PANEL_POSITION[0],
            self.PANEL_POSITION[1],
            self.PANEL_WIDTH,
            panel_height,
        )

        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=panel_rect,
            manager=self.ui_manager,
        )

        for index, option in enumerate(self.options):
            button = self._create_button(option.label, index)
            self.buttons[button] = option

        self.cancel_button = self._create_button(
            "Cancel",
            len(self.options),
        )

    def _create_button(
        self,
        text: str,
        index: int,
    ) -> pygame_gui.elements.UIButton:
        button_width, button_height = self.BUTTON_SIZE
        button_x = self.BUTTON_MARGIN
        button_y = self.BUTTON_MARGIN + index * (
            button_height + self.BUTTON_GAP
        )

        return pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                button_x,
                button_y,
                button_width,
                button_height,
            ),
            text=text,
            manager=self.ui_manager,
            container=self.panel,
        )

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        if event.ui_element == self.cancel_button:
            self.selected_construction = None
            return

        self.selected_construction = self.buttons.get(event.ui_element)

    def set_visible(self, visible: bool) -> None:
        if visible:
            self.panel.show()
        else:
            self.panel.hide()

    def get_selected_construction(self) -> ConstructionOption | None:
        return self.selected_construction
