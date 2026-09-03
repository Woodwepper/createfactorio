"""Application lifecycle and Pygame-ce main loop."""

import pygame

from client.config import TARGET_FPS, WINDOW_SIZE
from client.scenes.main_menu import MainMenuScene
from client.scenes.world_scene import WorldScene

from game.logic.core.world import World
from game.logic.core.simulation import Simulation


def run() -> None:
    """Run the application until the user closes it."""
    pygame.init()

    try:
        screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("Factory Simulator")

        clock = pygame.time.Clock()
        current_scene = MainMenuScene()
        is_app_running = True

        while is_app_running:
            # -----------------------------------------------------------------
            # Frame timing and input
            # -----------------------------------------------------------------
            delta_ms = clock.tick(TARGET_FPS)
            delta_seconds = delta_ms / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_app_running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    is_app_running = False

                current_scene.handle_event(event)

            # -----------------------------------------------------------------
            # Scene actions
            # -----------------------------------------------------------------
            action = current_scene.consume_requested_action()

            if action == "exit":
                is_app_running = False
            elif action == "create_world":
                world = World()
                simulation = Simulation(world, is_running=True)
                current_scene = WorldScene(world, simulation)
            elif action == "settings":
                print("Settings requested")

            # -----------------------------------------------------------------
            # Scene update and rendering
            # -----------------------------------------------------------------
            current_scene.update(delta_seconds)
            current_scene.draw(screen)
            pygame.display.flip()

    finally:
        pygame.quit()
