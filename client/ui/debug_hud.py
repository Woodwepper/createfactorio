"""Temporary debug HUD rendered by the client."""

import pygame

from game.logic.core.simulation import Simulation
from game.logic.core.world import World
from client.config import HUD_LINE_SPACING, HUD_POSITION, TEXT_COLOR


def render_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    world: World,
    simulation: Simulation,
    current_speed: int,
    accumulated_time: float,
    fps: float,
) -> None:
    """Render temporary simulation information in the top-left corner."""
    status = "Running" if simulation.is_running else "Paused"
    speed_text = f"x{current_speed}" if simulation.is_running else "Paused"

    hud_lines = [
        f"Tick: {world.get_tick_count()}",
        f"FPS: {fps:.2f}",
        f"Status: {status}",
        f"Speed: {speed_text}",
        f"Accumulated time: {accumulated_time:.3f}",
    ]

    for index, line in enumerate(hud_lines):
        text_surface = font.render(line, True, TEXT_COLOR)
        position = (
            HUD_POSITION[0],
            HUD_POSITION[1] + index * HUD_LINE_SPACING,
        )
        screen.blit(text_surface, position)
