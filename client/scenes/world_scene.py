import pygame
import pygame_gui

from client.config import (
    BACKGROUND_COLOR,
    FPS_DISPLAY_INTERVAL,
    MAX_SPEED,
    WINDOW_SIZE,
)
from client.scenes.scene import Scene
from client.simulation_clock import SimulationClock
from client.ui.debug_hud import render_hud
from client.rendering.grid_renderer import render_grid

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
        self.font = pygame.font.Font(None, 32)
        self.fps = 0.0
        self.fps_display_timer = 0.0
        self.fps_frame_count = 0

        self.ui_manager = pygame_gui.UIManager(WINDOW_SIZE)

        self.pause_button = self._create_button("Pause", 0)
        self.speed_plus_one_button = self._create_button("Speed +1", 1)
        self.speed_minus_one_button = self._create_button("Speed -1", 2)

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

    def handle_event(self, event: pygame.event.Event) -> None:
        self.ui_manager.process_events(event)

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.selected_cell = event.pos



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

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        render_grid(screen)

        render_hud(
            screen=screen,
            font=self.font,
            world=self.world,
            simulation=self.simulation,
            current_speed=self.speed,
            accumulated_time=self.simulation_clock.accumulated_time,
            fps=self.fps,
        )

        self.ui_manager.draw_ui(screen)

    def consume_requested_action(self) -> None:
        return None
