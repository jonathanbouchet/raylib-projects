from typing import Any
import pyray as pr
from .states import WaveStates


class Timer:
    def __init__(
        self,
        duration: int,
        repeat: bool = False,
        autostart: bool = False,
        func: Any = None,
    ) -> None:
        self.duration = (
            duration  # duration of the action / function the timer is tied to
        )
        self.repeat = repeat  # repeat the function every 'duration' seconds
        self.autostart = (
            autostart  # run the function once the timer object is instantianted
        )
        self.func = func  # function that is to be repeated
        self.active = False  # flag to denote the function is running

        if self.autostart:
            self.activate()

    def set_duration(self, new_duration: int) -> None:
        self.duration = new_duration

    def activate(self) -> None:
        """active only live until current time < duration"""
        self.active = True
        self.start_time = pr.get_time()

    def deactivate(self) -> None:
        """deactivate the timer"""
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def get_wave_time(self, wave_state: WaveStates) -> int:
        # if wave_state == WaveStates.SUCCESS:
        #     return -1
        return int(self.duration - (pr.get_time() - self.start_time))

    def update(self) -> None:
        if self.active:
            if pr.get_time() - self.start_time >= self.duration:
                if self.func:
                    # if self.func and self.start_time:
                    self.func()
                self.deactivate()
