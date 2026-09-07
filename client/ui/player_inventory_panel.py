import pygame
import pygame_gui

from client.config import WINDOW_SIZE
from game.logic.models.inventory_instance import InventoryInstance


class InventoryPanel:

    SLOT_COUNT = 27
    SLOT_COLUMNS = 9
    SLOT_SIZE = 70
    SLOT_GAP = 3
    SLOT_MARGIN = 3
    PANEL_INTERNAL_MARGIN = 3

    def __init__(self, manager, inventory: InventoryInstance):
        self.manager = manager
        self.inventory = inventory

        self.panel = pygame_gui.elements.UIPanel(
            self._get_rect(WINDOW_SIZE),
            manager=manager,
        )
        self.slots = []
        self._create_slots()
        self.refresh_slots()

        self.is_visible = False
        self.panel.hide()

    def _create_slots(self) -> None:
        self.slots = []
        for i in range(self.SLOT_COUNT):
            self.slots.append(self._create_slot(i))

    def _get_rect(self, window_size: tuple[int, int]) -> pygame.Rect:
        panel_width = (
            (self.SLOT_COLUMNS * self.SLOT_SIZE)
            + ((self.SLOT_COLUMNS - 1) * self.SLOT_GAP)
            + (2 * self.SLOT_MARGIN)
            + (2 * self.PANEL_INTERNAL_MARGIN)
        )

        rows = self.SLOT_COUNT // self.SLOT_COLUMNS
        panel_height = (
            (rows * self.SLOT_SIZE)
            + ((rows - 1) * self.SLOT_GAP)
            + (2 * self.SLOT_MARGIN)
            + (2 * self.PANEL_INTERNAL_MARGIN)
        )

        panel_x = (window_size[0] - panel_width) // 2
        panel_y = (window_size[1] - panel_height) // 2

        return pygame.Rect(panel_x, panel_y, panel_width, panel_height)

    def _create_slot(self, index: int) -> pygame_gui.elements.UIButton:
        slot_pos = self.get_slot_position(index)
        return pygame_gui.elements.UIButton(
            pygame.Rect(slot_pos[0], slot_pos[1], self.SLOT_SIZE, self.SLOT_SIZE),
            text="",
            manager=self.manager,
            container=self.panel,
        )

    def resize(self, window_size: tuple[int, int]) -> None:
        panel_rect = self._get_rect(window_size)
        self.panel.set_position(panel_rect.topleft)

    def refresh_slots(self) -> None:
        for index, slot_button in enumerate(self.slots):
            stack = self.inventory.get_slot(index)
            if stack is None:
                slot_button.set_text("")
            else:
                slot_button.set_text(
                    f"{stack.item_id}\n{stack.amount}"
                )

    def get_slot_position(self, index: int) -> tuple[int, int]:
        col = index % self.SLOT_COLUMNS
        row = index // self.SLOT_COLUMNS
        x = self.SLOT_MARGIN + col * (self.SLOT_SIZE + self.SLOT_GAP)
        y = self.SLOT_MARGIN + row * (self.SLOT_SIZE + self.SLOT_GAP)
        return (x, y)

    def toggle(self):
        self.is_visible = not self.is_visible
        if self.is_visible:
            self.panel.show()
        else:
            self.panel.hide()

    def handle_events(self, event):
        if event.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        for index, slot in enumerate(self.slots):
            if event.ui_element == slot:
                stack = self.inventory.get_slot(index)
                print(f"Slot {index + 1} clicked: {stack}")
                return
