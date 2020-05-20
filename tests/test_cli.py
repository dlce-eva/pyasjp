import pathlib

from pyasjp.__main__ import main


def test_diff(capsys):
    d = (pathlib.Path(__file__)).parent / 'data' / 'lists.txt'
    main(['diff', str(d), str(d)])
    out, _ = capsys.readouterr()
    assert not out
