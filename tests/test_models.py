import pytest

from pyasjp.models import *
from pyasjp.meanings import MEANINGS_ALL


def test_valid_strict_orthography():
    with pytest.raises(ValueError):
        valid_strict_orthography('t*a')


def test_Synset_from_txt(caplog):
    ss = Synset.from_txt('1. I\tXXX / a comment/')
    assert not ss.words
    assert ss.meaning_id == 1
    assert ss.comment == 'a comment'

    assert not Synset.from_txt('1 I\tABC //').words
    assert caplog.records


def test_Doculect_asjp_name():
    dl = Doculect.from_txt(""""ESK_A'Y/AN{F.G|@}\n 1    9.43  124.24          -1         esy""")
    assert dl.asjp_name == 'ESK_AY_AN'


def test_roundtrip():
    txt = """\
ESKAYAN{Oth.UNCLASSIFIED|Mixedlanguage,Cebuano-Spanish-English@ArtificialLanguage}
 1    9.43  124.24          -1         esy
1 I\tnarin //
2 you\tsamo //
3 we\tarh~itika //
11 one\toy //
12 two\t%tri //
18 person\tbolto //
19 fish\t%pir //
21 dog\tplodo //
22 louse\thoko //
23 tree\tXXX //
25 leaf\tsaliti, %daloha //
28 skin\t%pil //
30 blood\talw~atis //
31 bone\tgiro //
34 horn\tXXX //
39 ear\tklabara //
40 eye\tsim //
41 nose\tjiomint~ir //
43 tooth\tprind~ido //
44 tongue\tgolitas //
47 knee\tilkdo //
48 hand\tdapami //
51 breast\tpalda //
53 liver\twas //
54 drink\tojirim, porx~irim //
57 see\tmosimsati //
58 hear\tyant~isi //
61 die\tmodowati //
66 come\tlari, kimtak //
72 sun\t%astro //
74 star\tpisakol //
75 water\tkoly~ar //
77 stone\tsabana //
82 fire\tpolo7iso //
85 path\trakilan //
86 mountain\tXXX //
92 night\tkloper //
95 full\tXXX //
96 new\ttibil //
100 name\tlaNg~is, laNis //"""
    assert txt == Doculect.from_txt(txt).to_txt(add_missing=True)


def test_fixing():
    txt = """\
ZHAOZHUANG_BAI{ST.BAI|Sino-Tibetan,Tibeto-Burman,NortheasternTibeto-Burman,Bai@}
 1   25.56  100.26      400000   bai   bfs
1 I	No //
2 we	5a //
3 water	sy~i //
12 tree	cu //
42 tooth	ci pa //
43 tongue	ce //
75 two	ko, ne //
85 person	5i ka //
100 name	mia //"""
    dl = Doculect.from_txt(txt)
    reverse_lookup = {v: k for k, v in MEANINGS_ALL.items()}
    for ss in dl.synsets:
        if ss.meaning in reverse_lookup:
            ss.meaning_id = reverse_lookup[ss.meaning]
    assert str(dl) == """\
ZHAOZHUANG_BAI{ST.BAI|Sino-Tibetan,Tibeto-Burman,NortheasternTibeto-Burman,Bai@}
 1   25.56  100.26      400000   bai   bfs
1 I	No //
3 we	5a //
12 two	ko, ne //
18 person	5i ka //
23 tree	cu //
43 tooth	ci pa //
44 tongue	ce //
75 water	sy~i //
100 name	mia //"""
