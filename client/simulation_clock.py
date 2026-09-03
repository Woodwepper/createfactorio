"""Scheduling for simulation ticks on the client side."""

from dataclasses import dataclass

from client.config import SPEED_INTERVALS


@dataclass
class SimulationClock:
    """Track elapsed time and decide when the next simulation tick is due."""

    speed: int = 1
    accumulated_time: float = 0.0

    def set_speed(self, speed: int) -> None:
        if speed not in SPEED_INTERVALS:
            raise ValueError(f"Unsupported simulation speed: {speed}")

        self.speed = speed

    def should_tick(self, delta_seconds: float, is_running: bool) -> bool:
        if not is_running:
            return False

        self.accumulated_time += delta_seconds
        tick_interval = SPEED_INTERVALS[self.speed]

        if self.accumulated_time < tick_interval:
            return False

        self.accumulated_time -= tick_interval
        return True
