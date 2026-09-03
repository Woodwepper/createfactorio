"""Keyboard input handling for the temporary simulation controls."""

import pygame


def handle_events(
    events: list[pygame.event.Event],
    current_speed: int,
    is_simulation_running: bool,
) -> tuple[bool, int, bool]:
    """Process application and simulation keyboard controls.

    Returns:
        A tuple containing application state, selected speed, and simulation state.
    """
    is_app_running = True

    for event in events:
        if event.type == pygame.QUIT:
            is_app_running = False
            continue

        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            is_app_running = False
        elif event.key == pygame.K_0:
            is_simulation_running = False
        elif event.key in (
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
        ):
            current_speed = event.key - pygame.K_0
            is_simulation_running = True

    return is_app_running, current_speed, is_simulation_running
