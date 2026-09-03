from dataclasses import dataclass
from .world import World

@dataclass
class Simulation:
    world: World
    is_running: bool = False

    def tick(self):
        if not self.is_running:
            return
        self.world.update()
