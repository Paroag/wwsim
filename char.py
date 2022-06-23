from wwsim.event import Event


class Char:

    def __init__(
            self,
            sp,
            crit=0,
            vers=0,
            haste=0,
    ):
        self.sp = sp
        self.crit = crit
        self.vers = vers
        self.haste = haste

    def get_haste_modifier(self):
        return 1/(1+self.haste/100)

    def update(self, event: Event):
        return []
