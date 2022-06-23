import logging
import random

from wwsim.druid.balance.balance import Wrath, Starfall, Balance
from wwsim.sim import Sim

random.seed(0)
logging.basicConfig(level=logging.DEBUG)
char = Balance(sp=100, haste=0, crit=0, vers=0)
spl_seq = [Wrath(), Wrath()] + [Starfall()]*7 + [Wrath()]
sim = Sim(char, spl_seq)
sim.run()
