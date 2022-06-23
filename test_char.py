from wwsim.char import Char


def test_get_haste_modifier():
    char = Char(sp=100, haste=50)
    assert char.get_haste_modifier() == 2/3
