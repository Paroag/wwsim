from typing import Callable

from wwsim.event import Event


class Buff(Event):

    def __init__(self, name=None, duration=0, effect: Callable = None):
        self.base_duration = duration
        self.real_duration = duration
        self.effect = effect
        super().__init__(name)

    def __eq__(self, other):
        return self.name == other.name

    def forward_time(self, delta_t):
        self.real_duration -= delta_t

    def refresh(self):
        self.real_duration = min(
            1.3 * self.base_duration,
            self.real_duration + self.base_duration
        )
