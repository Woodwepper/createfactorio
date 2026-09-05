import pygame
import pygame_gui

from client.config import (
    BACKGROUND_COLOR,
    FPS_DISPLAY_INTERVAL,
    FONT_SIZE,
    MAX_SPEED,
    WINDOW_SIZE,
    GRID_CELL_SIZE,
)
from client.scenes.scene import Scene
from client.simulation_clock import SimulationClock
from client.ui.debug_hud import render_hud
from client.rendering.grid_renderer import render_grid
from client.ui.construction_menu import ConstructionMenu
from client.ui.inventory_panel import InventoryPanel
from game.logic.orders.place_construction_order import PlaceConstructionOrder

class WorldScene(Scene):
    """Temporary scene for the active world and simulation."""

    BUTTON_SIZE = (200, 50)
    BUTTON_GAP = 10
    BUTTON_MARGIN = 20

    def __init__(self, world, simulation):
        self.world = world
        self.simulation = simulation

        self.speed = 1
        self.simulation_clock = SimulationClock(self.speed)
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.fps = 0.0
        self.fps_display_timer = 0.0
        self.fps_frame_count = 0

        self.ui_manager = pygame_gui.UIManager(WINDOW_SIZE)

        self.pause_button = self._create_button("Pause", 0)
        self.speed_plus_one_button = self._create_button("Speed +1", 1)
        self.speed_minus_one_button = self._create_button("Speed -1", 2)

        self.construction_menu = ConstructionMenu(
            self.ui_manager,
            self.world.definitions.get_construction_options(),
        )
        self.inventory_panel = InventoryPanel(
            self.ui_manager,
            self.world.player_inventory,
        )

        self.hovered_cell = None
        self.selected_cell = None

    def _create_button(self, text: str, index: int) -> pygame_gui.elements.UIButton:
        button_width, button_height = self.BUTTON_SIZE
        total_width = (button_width * 3) + (self.BUTTON_GAP * 2)
        first_x = WINDOW_SIZE[0] - total_width - self.BUTTON_MARGIN
        button_x = first_x + index * (button_width + self.BUTTON_GAP)
        button_y = self.BUTTON_MARGIN

        rect = pygame.Rect(
            button_x,
            button_y,
            button_width,
            button_height,
        )

        return pygame_gui.elements.UIButton(
            relative_rect=rect,
            text=text,
            manager=self.ui_manager,
        )

    def _draw_hovered_cell(self, screen: pygame.Surface) -> None:
        if self.hovered_cell is None:
            return

        column, row = self.hovered_cell
        x = column * GRID_CELL_SIZE
        y = row * GRID_CELL_SIZE

        selection_surface = pygame.Surface((GRID_CELL_SIZE, GRID_CELL_SIZE), pygame.SRCALPHA)
        selection_surface.fill((255, 255, 255, 64))
        screen.blit(selection_surface, (x, y))

    def get_cell(self, x: int, y: int) -> tuple[int, int]:
        column = x // GRID_CELL_SIZE
        row = y // GRID_CELL_SIZE
        return column, row

    def handle_event(self, event: pygame.event.Event) -> None:
        self.ui_manager.process_events(event)
        self.construction_menu.handle_events(event)
        self.inventory_panel.handle_events(event)

        if event.type == pygame.VIDEORESIZE:
            self.ui_manager.set_window_resolution(event.size)
            self.inventory_panel.resize(event.size)
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.inventory_panel.toggle()
            self.construction_menu.set_visible(
                not self.inventory_panel.is_visible
            )
            self.hovered_cell = None
            return

        if event.type == pygame.MOUSEMOTION:
            if self.ui_manager.get_hovering_any_element():
                self.hovered_cell = None
                return

            x, y = event.pos
            self.hovered_cell = self.get_cell(x, y)
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.ui_manager.get_hovering_any_element():
                return

            selected_construction = (
                self.construction_menu.get_selected_construction()
            )
            if selected_construction is None:
                return

            x, y = event.pos
            self.selected_cell = self.get_cell(x, y)

            order = PlaceConstructionOrder(
                construction_type=selected_construction.construction_type,
                definition_id=selected_construction.definition_id,
                cell=self.selected_cell,
            )
            self.simulation.order_system.enqueue(order)

        if event.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        if event.ui_element == self.pause_button:
            self.simulation.is_running = not self.simulation.is_running
            self._update_pause_button_text()

        elif event.ui_element == self.speed_plus_one_button:
            self.speed = min(MAX_SPEED, self.speed + 1)
            self.simulation_clock.set_speed(self.speed)
            self.simulation.is_running = True
            self._update_pause_button_text()

        elif event.ui_element == self.speed_minus_one_button:
            self.speed = max(1, self.speed - 1)
            self.simulation_clock.set_speed(self.speed)
            self.simulation.is_running = True
            self._update_pause_button_text()


    def _update_pause_button_text(self) -> None:
        text = "Pause" if self.simulation.is_running else "Resume"
        self.pause_button.set_text(text)

    def update(self, delta_seconds: float) -> None:
        self.ui_manager.update(delta_seconds)

        self.fps_frame_count += 1
        self.fps_display_timer += delta_seconds
        if self.fps_display_timer >= FPS_DISPLAY_INTERVAL:
            self.fps = self.fps_frame_count / self.fps_display_timer
            self.fps_frame_count = 0
            self.fps_display_timer -= FPS_DISPLAY_INTERVAL

        if self.simulation_clock.should_tick(
            delta_seconds,
            self.simulation.is_running,
        ):
            self.simulation.tick()

        self.inventory_panel.refresh_slots()

    def _draw_buildings(self, screen: pygame.Surface) -> None:
        for cell in self.world.buildings:
            column, row = cell
            rect = pygame.Rect(
                column * GRID_CELL_SIZE,
                row * GRID_CELL_SIZE,
                GRID_CELL_SIZE,
                GRID_CELL_SIZE,
            )
            pygame.draw.rect(screen, (90, 120, 160), rect)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        render_grid(screen)
        self._draw_buildings(screen)

        self._draw_hovered_cell(screen)

        render_hud(
            screen=screen,
            font=self.font,
            world=self.world,
            simulation=self.simulation,
            current_speed=self.speed,
            accumulated_time=self.simulation_clock.accumulated_time,
            fps=self.fps,
            selected_cell=self.selected_cell,
            hovered_cell=self.hovered_cell,
            selected_building=(
                self.construction_menu.selected_construction.definition_id
                if self.construction_menu.selected_construction is not None
                else None
            ),
        )

        self.ui_manager.draw_ui(screen)

    def consume_requested_action(self) -> None:
        return None
