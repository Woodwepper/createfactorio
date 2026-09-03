from dataclasses import dataclass

@dataclass
class World:
    tick_count: int = 0

    def update(self):
        self.tick_count += 1

    def get_tick_count(self):
        return self.tick_count
