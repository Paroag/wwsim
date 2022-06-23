import logging

from wwsim import GCD
from wwsim.buff import Buff
from wwsim.char import Char
from wwsim.debuff import Dot
from wwsim.event import Event
from wwsim.spl import Spl

logging.getLogger(__name__)


class Druid(Char):
    pass


class Balance(Druid):

    def __init__(self, *args, astral_power=0, **kwargs):
        self.astral_power = astral_power
        self.starfall_left = 2
        self.wrath_left = 2
        super().__init__(*args, **kwargs)

    def update(self, event: Event):
        if event == "starfall":
            if self.starfall_left > 0:
                self.starfall_left -= 1
                if self.starfall_left == 0:
                    logging.debug(f"Entering solar eclipse")
                    return [SolarEclipse()]
        if event == "wrath":
            if self.wrath_left > 0:
                self.wrath_left -= 1
                if self.wrath_left == 0:
                    logging.debug(f"Entering lunar eclipse")
                    return [LunarEclipse()]
        if hasattr(event, "astral_power"):
            self.astral_power = min(100, self.astral_power + event.astral_power)
            if self.astral_power < 0:
                raise ValueError("You do not have enough astral power")

        return []


class Wrath(Spl):
    def __init__(self):
        super().__init__(
            name="wrath",
            spl_coef=0.6,
            cast_t=1.5,
        )
        self.astral_power = 6


class Starfall(Spl):
    def __init__(self):
        super().__init__(
            name="starfall",
            spl_coef=0.75,
            cast_t=2,
        )
        self.astral_power = 8


class MoonfireTick(Dot):
    def __init__(self):
        super().__init__(
            name="moonfire_ticks",
            dot_coef=1.218,
            duration=14,
            interval=2,
        )


class Moonfire(Spl):
    def __init__(self):
        super().__init__(
            name="moonfire",
            spl_coef=0.2,
            cast_t=GCD,
            debuff=MoonfireTick()
        )
        self.astral_power = 2


class Starsurge(Spl):
    def __init__(self):
        super().__init__(
            name="starsurge",
            spl_coef=2.07,
            cast_t=GCD,
        )
        self.astral_power = -30


def solar_eclipse(event: Event):
    if isinstance(event, Spl) and event == "wrath":
        event.cast_t *= 0.92
        event.spl_coef *= 1.2


class SolarEclipse(Buff):

    def __init__(self):
        super().__init__(
            name="lunar_eclipse",
            duration=15,
            effect=solar_eclipse,
        )


def lunar_eclipse(event: Event):
    if isinstance(event, Spl) and event == "starfall":
        event.cast_t *= 0.92
        event.bonus_crit += 20


class LunarEclipse(Buff):

    def __init__(self):
        super().__init__(
            name="lunar_eclipse",
            duration=15,
            effect=lunar_eclipse,
        )
