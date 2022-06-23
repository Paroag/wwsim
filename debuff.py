from wwsim.event import Event


class Debuff(Event):

    def __init__(self, name=None, duration=0):
        self.base_duration = duration
        self.real_duration = duration
        super().__init__(name)

    def forward_time(self, delta_t):
        self.real_duration -= delta_t

    def refresh(self):
        self.real_duration = min(
            1.3 * self.base_duration,
            self.real_duration + self.base_duration
        )


class Dot(Debuff):

    def __init__(
        self,
        name=None,
        dot_coef=0,
        duration=0,
        interval=1,
    ):
        self.dot_coef = dot_coef
        self.interval = interval
        self.last_tick = None
        super().__init__(name, duration)

    def tick(self, t):
        dmg = self.dot_coef * self.interval / self.base_duration
        self.last_tick = t
        return dmg
