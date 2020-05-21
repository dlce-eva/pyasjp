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


def test_Doculect_formatted():
    dl = Doculect.from_txt("""\
BEDJA_BEDAWI{AA.BEJA|Afro-Asiatic,Cushitic,North@Afro-Asiatic,Cushitic}
 3   19.00   36.00     3364000   bej   bej
1 I\tane, heb //
2 you\tuk, ukna //
3 we\ton, hon, henen, un //
4 this\tXXX //
5 that\tXXX //
6 who\taw //
7 what\tXXX //
8 not\tXXX //
9 all\tka, natka, kassu, karsu //
10 many\tXXX //
11 one\tgal, gat //
12 two\tmale, malo //
13 big\tXXX //
14 long\tgw~imad //
15 small\tdabali, dibili, dis //
16 woman\tamna //
17 man\tXXX //
18 person\tXXX //
19 fish\taSi, aSob, aSoyay, aSoyey //
21 dog\tyas //
22 louse\tibab, tat //
23 tree\tXXX //
24 seed\tfar, tera //
25 leaf\tXXX //
26 root\tday, dey, gadam, gadama, niwa //
27 bark\tSakar //
28 skin\tgale, sar //
30 blood\tboy //
31 bone\tmitat //
32 grease\tsimum, wadak //
33 egg\tkw~hi, sukw~m, sukma //
34 horn\td7a //
35 tail\tniwa //
36 feather\tlat, timba //
37 hair\thamoyiay //
38 head\tgirma, gilma //
39 ear\tangw~il //
40 eye\tgw~7ad, lili //
41 nose\tginuf, genuf, genif //
42 mouth\tyaf, yafa //
43 tooth\tkw~ire //
44 tongue\thadid, hadida, midab, midalab //
45 claw\tXXX //
46 foot\tlagad //
47 knee\tXXX //
48 hand\tXXX //
49 belly\tXXX //
50 neck\t7ala, mok, moka //
51 breast\tXXX //
52 heart\tgug, guga //
53 liver\tse, si //
54 drink\tgibit, gw~iham, gw~ham, nagaram, simham, sirmam, Sifi, yasum //
55 eat\ttam //
56 bite\tfinik //
57 see\terh, irh, reh, rih //
58 hear\tmasu, masiw //
59 know\tkan //
60 sleep\tdiw //
61 die\tyay //
62 kill\tdir //
63 swim\tXXX //
64 fly\tXXX //
65 walk\thirer, tabbek, tilil //
66 come\t7i //
67 lie\tXXX //
68 sit\tXXX //
69 stand\tXXX //
70 give\tgana, hiw, nun //
71 say\tXXX //
72 sun\tXXX //
73 moon\teterig, terig, tirig, terga //
74 star\thayuk, hayikw~ //
75 water\tXXX //
76 rain\tbire, sif, tab, taba, wiya //
77 stone\t7awe, 7aweb //
78 sand\tXXX //
79 earth\tXXX //
80 cloud\tbal, bala, sab, sahab //
81 smoke\teda, ega //
82 fire\tn7e //
83 ash\thamiS, n7et haS, n7ethas //
84 burn\tbalol, liw //
85 path\tsalal, salla, salala //
86 mountain\treba, riba //
87 red\tXXX //
88 green\tsota //
89 yellow\tXXX //
90 white\tXXX //
91 black\tXXX //
92 night\thawad //
95 full\tatab //
96 new\tXXX //
97 good\tdai, Sibi, Sibo, Sibob //
98 round\tXXX //
99 dry\teSa, balam, balama //
100 name\tsim, sima //
""")
    assert dl.get(1)
    assert dl.to_formatted_row() == [
        'BEDJA_BEDAWI',
        'AA',
        'BEJA',
        'Afro-Asiatic,Cushitic,North',
        'Afro-Asiatic,Cushitic',
        '19.00',
        '36.00',
        '3364000',
        'bej',
        'bej',
        'ane, heb',
        'uk, ukna',
        'on, hon, henen, un',
        'XXX',
        'XXX',
        'aw',
        'XXX',
        'XXX',
        'ka, natka, kassu, karsu',
        'XXX',
        'gal, gat',
        'male, malo',
        'XXX',
        'gw~imad',
        'dabali, dibili, dis',
        'amna',
        'XXX',
        'XXX',
        'aSi, aSob, aSoyay, aSoyey',
        'XXX',
        'yas',
        'ibab, tat',
        'XXX',
        'far, tera',
        'XXX',
        'day, dey, gadam, gadama, niwa',
        'Sakar',
        'gale, sar',
        'XXX',
        'boy',
        'mitat',
        'simum, wadak',
        'kw~hi, sukw~m, sukma',
        'd7a',
        'niwa',
        'lat, timba',
        'hamoyiay',
        'girma, gilma',
        'angw~il',
        'gw~7ad, lili',
        'ginuf, genuf, genif',
        'yaf, yafa',
        'kw~ire',
        'hadid, hadida, midab, midalab',
        'XXX',
        'lagad',
        'XXX',
        'XXX',
        'XXX',
        '7ala, mok, moka',
        'XXX',
        'gug, guga',
        'se, si',
        'gibit, gw~iham, gw~ham, nagaram, simham, sirmam, Sifi, yasum',
        'tam',
        'finik',
        'erh, irh, reh, rih',
        'masu, masiw',
        'kan',
        'diw',
        'yay',
        'dir',
        'XXX',
        'XXX',
        'hirer, tabbek, tilil',
        '7i',
        'XXX',
        'XXX',
        'XXX',
        'gana, hiw, nun',
        'XXX',
        'XXX',
        'eterig, terig, tirig, terga',
        'hayuk, hayikw~',
        'XXX',
        'bire, sif, tab, taba, wiya',
        '7awe, 7aweb',
        'XXX',
        'XXX',
        'bal, bala, sab, sahab',
        'eda, ega',
        'n7e',
        'hamiS, n7et haS, n7ethas',
        'balol, liw',
        'salal, salla, salala',
        'reba, riba',
        'XXX',
        'sota',
        'XXX',
        'XXX',
        'XXX',
        'hawad',
        'XXX',
        'XXX',
        'atab',
        'XXX',
        'dai, Sibi, Sibo, Sibob',
        'XXX',
        'eSa, balam, balama',
        'sim, sima'
    ]
    assert len(dl.formatted_header()) == 110


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
