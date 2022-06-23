import logging
import random
from typing import List

from wwsim import GCD
from wwsim.buff import Buff
from wwsim.char import Char
from wwsim.debuff import Debuff, Dot
from wwsim.spl import Spl

logger = logging.getLogger(__name__)


class Sim:

    def __init__(self, char: Char, spl_seq: List[Spl]):
        self.char = char
        self.spl_seq = spl_seq
        self.events_seq = {}
        self.buffs = []
        self.t = 0
        self.dmg = 0

    def resolve_next_event(self):

        ###
        # INITIALIZE, END CONDITION
        ###
        if not self.events_seq:
            if not self.spl_seq:
                return None
            self.events_seq[0] = self.spl_seq.pop(0)

        ###
        # FIND NEXT EVENT, UPDATE TIME
        ###
        events = sorted(self.events_seq.items())
        current_t, event = events[0]

        self.forward_time(delta_t=current_t - self.t)
        self.t = current_t

        ###
        # SPL CASE
        ###
        if isinstance(event, Spl):
            dmg = self.deal_spl_dmg(self.char, event, self.buffs)
            logging.debug(f"[{round(self.t, 2)}] casting spell {event} for {round(dmg, 2)} damage.")
            if event.debuff and isinstance(event.debuff, Dot):
                debuff = self.find_debuff(event.debuff)
                if debuff is not None:
                    debuff.refresh()
                else:
                    self.events_seq[self.t + event.debuff.interval*self.char.get_haste_modifier()] = event.debuff
            if self.spl_seq:
                self.events_seq[self.t+max(GCD, event.cast_t)*self.char.get_haste_modifier()] = self.spl_seq.pop(0)
            new_buffs = self.char.update(event)
            for buff in new_buffs:
                self.events_seq[self.t+buff.real_duration] = buff
            self.buffs += new_buffs

        ###
        # DOT CASE
        ###
        if isinstance(event, Dot):
            coef = 1
            if event.last_tick is not None and self.t - event.last_tick < event.interval * self.char.get_haste_modifier():
                #We are dealing with a partial tick
                coef = (self.t - event.last_tick)/(event.interval * self.char.get_haste_modifier())
            dmg = self.deal_dot_dmg(self.char, event, self.buffs)
            dmg *= coef
            logging.debug(f"[{round(self.t, 2)}] {event} ticking for {round(dmg, 2)} damage.")
            self.events_seq[self.t+min(event.interval*self.char.get_haste_modifier(), event.real_duration)] = event

        ###
        # BUFF CASE
        ###
        if isinstance(event, Buff):
            self.buffs = [buff for buff in self.buffs if not buff == event]

        del self.events_seq[self.t]
        return True

    def deal_spl_dmg(self, char: Char, spl: Spl, buffs: List[Buff]):
        for buff in buffs:
            buff.effect(spl)
        dmg = self.char.sp * spl.spl_coef
        dmg *= 2 if random.uniform(0, 100) < char.crit + spl.bonus_crit else 1
        dmg *= 1 + char.vers/100
        self.dmg += dmg
        return round(dmg, 2)

    def deal_dot_dmg(self, char: Char, dot: Dot, buffs: List[Buff]):
        for buff in buffs:
            buff.effect(dot)
        dmg = self.char.sp * dot.tick(self.t)
        dmg *= 2 if random.uniform(0, 100) < char.crit else 1
        dmg *= 1 + char.vers / 100
        self.dmg += dmg
        return round(dmg, 2)

    def find_debuff(self, debuff: Debuff):
        for t, event in self.events_seq.items():
            if isinstance(event, Debuff) and event.name == debuff.name:
                return event

    def forward_time(self, delta_t):
        for event in self.events_seq.values():
            event.forward_time(delta_t)

    def run(self):
        while self.resolve_next_event():
            pass
