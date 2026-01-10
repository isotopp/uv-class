from __future__ import annotations

from helloext import hellop, hellos


def test_hellos():
    assert hellos("Kris") == "Hello, Kris"


def test_hellop(capsys):
    hellop("Kris")
    captured = capsys.readouterr()
    assert captured.out == "Hello, Kris\n"

