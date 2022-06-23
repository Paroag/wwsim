from typing import Optional

from wwsim.debuff import Debuff
from wwsim.event import Event


class Spl(Event):

    def __init__(
            self,
            name,
            spl_coef=0,
            cast_t=0,
            debuff: Optional[Debuff] = None,
    ):
        self.spl_coef = spl_coef
        self.cast_t = cast_t
        self.debuff = debuff
        self.bonus_crit = 0

        super(Spl, self).__init__(name)
