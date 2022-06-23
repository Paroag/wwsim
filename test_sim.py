import random

import pytest

from wwsim.druid.balance.balance import Moonfire, Wrath, Starfall, Balance, Starsurge
from wwsim.char import Char
from wwsim.sim import Sim


@pytest.fixture
def char():
    return Char(sp=100)


def test_wrath(char):
    spl_seq = [Wrath(), Wrath()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.dmg == 120


def test_moonfire(char):
    spl_seq = [Moonfire()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.dmg == pytest.approx(141.8)
    assert sim.t == 14


def test_moonfire_partial_tick(char):
    spl_seq = [Moonfire(), Moonfire()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.dmg == pytest.approx(211.4, 0.1)
    assert sim.t == 19.7


def test_wrath_crit():
    random.seed(0)
    char = Char(sp=100, crit=30)
    spl_seq = [Wrath()]*1000
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.dmg == 77760


def test_moonfire_crit():
    random.seed(0)
    char = Char(sp=100, crit=30)
    spl_seq = [Moonfire()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.dmg == pytest.approx(159.2)


def test_wrath_vers():
    char = Char(sp=100, vers=25)
    spl_seq = [Wrath()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.dmg == 75


def test_moonfire_vers():
    char = Char(sp=100, vers=30)
    spl_seq = [Moonfire()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.dmg == pytest.approx(184.34)


def test_wrath_crit_vers():
    random.seed(0)
    char = Char(sp=100, crit=30, vers=25)
    spl_seq = [Wrath()]*1000
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.dmg == 97200


def test_wrath_haste():
    char = Char(sp=100, haste=50)
    spl_seq = [Wrath(), Wrath()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.dmg == 120
    assert sim.t == 1


def test_moonfire_haste():
    char = Char(sp=100, haste=100)
    spl_seq = [Moonfire(), Moonfire()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.t == 18.95
    assert sim.dmg == pytest.approx(370.0, 0.1)


def test_eclipse():
    char = Balance(sp=100)
    spl_seq = [Starfall(), Starfall(), Wrath()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.t == 17
    assert sim.dmg == pytest.approx(222, 0.1)


def test_astral_power():
    char = Balance(sp=100)
    spl_seq = [Wrath(), Starfall(), Moonfire()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert char.astral_power == 16


def test_not_enough_astral_power():
    char = Balance(sp=100)
    spl_seq = [Wrath(), Starfall(), Moonfire(), Starsurge()]
    sim = Sim(char, spl_seq)
    with pytest.raises(ValueError):
        sim.run()


def test_full_cast():
    random.seed(0)
    char = Char(sp=100, haste=30, crit=50, vers=30)
    spl_seq = [Wrath(), Moonfire(), Wrath(), Starfall()]
    sim = Sim(char, spl_seq)
    sim.run()

    assert sim.t == pytest.approx(15.2, 0.1)
    assert sim.dmg == pytest.approx(696.8, 0.1)

