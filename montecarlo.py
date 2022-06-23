import copy
import random

from wwsim.druid.balance.balance import Balance, Moonfire, Wrath, Starfall
from wwsim.sim import Sim

SPL_POOL = [Moonfire, Wrath, Starfall]
lines = []
for k in range(100000):
    char = Balance(sp=100) #, crit=30, haste=30, vers=30)
    spl_seq = [spl_class() for spl_class in random.choices(SPL_POOL, k=30)]
    sim = Sim(char, copy.deepcopy(spl_seq))
    sim.run()
    lines += [
        ";".join(
            [
                str(round(sim.dmg/sim.t, 2)),
                str(round(sim.dmg, 2)),
                str(round(sim.t, 2))
            ] + [
                spl.name for spl in spl_seq
            ]
        )
        + "\n"
    ]

with open("result.csv", "a") as f:
    f.writelines(lines)

