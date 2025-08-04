import pathlib

from pyasjp.__main__ import main


def test_formatted(tmp_path):
    o = tmp_path / 'out.tab'
    d = (pathlib.Path(__file__)).parent / 'data' / 'lists.txt'
    main(['formatted', str(d), str(o)])
    assert o.exists()


def test_diff(capsys, tmp_path):
    d = (pathlib.Path(__file__)).parent / 'data' / 'lists.txt'
    main(['diff', str(d), str(d)])
    out, _ = capsys.readouterr()
    assert not out

    d2 = tmp_path / 'l.txt'
    d2.write_text(
        '\n'.join(l.replace('n!~a', 'n!~aaa') for i, l in
                  enumerate(d.read_text(encoding='cp1252').split('\n'))),
        encoding='cp1252')
    main(['diff', str(d), str(d2)])
    out, _ = capsys.readouterr()
    assert 'GWI' in out
