import pytest

from wwsim.druid.balance.balance import MoonfireTick


def test_skip_time():
    debuff = MoonfireTick()
    debuff.forward_time(10)

    assert debuff.real_duration == 4


def test_tick():
    debuff = MoonfireTick()
    dmg = debuff.tick(0)

    assert debuff.last_tick == 0
    assert dmg == pytest.approx(1.218/7)


def test_refresh():
    debuff = MoonfireTick()
    debuff.real_duration = 2
    debuff.refresh()

    assert debuff.real_duration == 16


def test_refresh_pandemic():
    debuff = MoonfireTick()
    debuff.refresh()

    assert debuff.real_duration == 18.2
