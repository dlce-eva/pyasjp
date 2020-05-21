import pathlib

from pyasjp.__main__ import main


def test_formatted(tmpdir):
    o = pathlib.Path(str(tmpdir)) / 'out.tab'
    d = (pathlib.Path(__file__)).parent / 'data' / 'lists.txt'
    main(['formatted', str(d), str(o)])
    assert o.exists()


def test_diff(capsys):
    d = (pathlib.Path(__file__)).parent / 'data' / 'lists.txt'
    main(['diff', str(d), str(d)])
    out, _ = capsys.readouterr()
    assert not out
