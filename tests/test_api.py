import pathlib

import pytest

from pyasjp.models import Doculect
from pyasjp.api import ASJP


@pytest.fixture
def repos():
    return pathlib.Path(__file__).parent / 'data'


def test_ASJP_iter_doculects(repos):
    api = ASJP(repos)
    dls = list(api.iter_doculects())
    gwi = dls[0]
    assert str(gwi).startswith('GWI')
    assert api.source(gwi) and api.transcriber(gwi)


def test_ASJP_to_text(repos):
    api = ASJP(repos)
    res = api.to_txt(
        Doculect.from_txt('A{F.H|x@y}\n 1    9.43  124.24          -1         esy\n1 I\ti //'),
        Doculect.from_txt('B{F.G1|x@y}\n 1    9.43  124.24       -1910         esy\n1 I\ti //'),
        Doculect.from_txt('C{F.G1|x@y}\n 1    9.43  124.24       -1910         esy\n1 I\ti //'),
        Doculect.from_txt('D{A.G2|x@y}\n 1    9.43  124.24          -2         esy\n1 I\ti //'),
    )
    # Make sure doculects are ordered by WALS classification and the corresponding marker is set.
    assert res.split('\n\n')[-1].strip() == """\
D{A.G2|x@y}
 3    9.43  124.24          -2         esy
1 I	i //
B{F.G1|x@y}
 3    9.43  124.24       -1910         esy
1 I	i //
C{F.G1|x@y}
 1    9.43  124.24       -1910         esy
1 I	i //
A{F.H|x@y}
 2    9.43  124.24          -1         esy
1 I	i //"""
