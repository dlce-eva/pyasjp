import re
import logging
import collections
import dataclasses
from typing import Optional

from clldutils.misc import nfilter

from pyasjp.meanings import MEANINGS, MEANINGS_ALL

__all__ = [
    'Transcriber', 'Source', 'Word', 'Synset', 'Doculect', 'ASJPCODES', 'txt_header',
    'valid_strict_orthography',
]

# see
# Brown, Cecil H., Eric W. Holman, Søren Wichmann, and Viveka Vilupillai. 2008.
# Automated classification of the world’s languages:
# a description of the method and preliminary results.
# STUF – Language Typology and Universals 61:285-308.
CONSONANTS = 'pbfvmw8tdszcnrlSZCjT5ykgxNqXh7L4G!'
VOWELS = 'ieE3auo'
ASJPCODES = CONSONANTS + VOWELS
MODIFIERS = ''.join([
    "*",  # An asterisk following any one of the seven vowel symbols indicates vowel nasalization.
    "~",  # A modifier that follows two juxtaposed consonants.
    "$",  # Similar ~ except that it follows three juxtaposed consonants.
    '"',  # Immediately follows a consonant that is glottalized.
])
PUNCTUATION = " "
WORD_PATTERN = re.compile('[{}]+'.format(re.escape(ASJPCODES + MODIFIERS + PUNCTUATION)))
MISSING_WORD = 'XXX'
LANGUAGE_LINE_PATTERN = re.compile(
    r'(?P<name>[^{]+){(?P<w>[^|]*)\|(?P<e>[^@}]*)(@(?P<g>[^}]*))?}?')


def valid_strict_orthography(word):
    for modifier, modified in [
        ('*', VOWELS),
        ('~', CONSONANTS),
        ('$', CONSONANTS),
        ('"', CONSONANTS),
    ]:
        if re.search('(?<![{}]){}'.format(re.escape(modified), re.escape(modifier)), word):
            raise ValueError('Misplaced modifier: {}'.format(word))


@dataclasses.dataclass
class Transcriber:
    id: str
    name: str


@dataclasses.dataclass
class Source:
    id: str
    asjp_name: str
    author: str
    year: str
    title_etc: str
    list_made_by: list[str]

    def __post_init__(self):
        self.list_made_by = nfilter([ss.strip() for ss in re.split(r'/|->', self.list_made_by)])


@dataclasses.dataclass
class Word:
    form: str
    loan: bool

    def __post_init__(self):
        assert WORD_PATTERN.fullmatch(self.form), self.form
        assert isinstance(self.loan, bool)

    @classmethod
    def from_txt(cls, txt):
        if txt.startswith('%'):
            return cls(form=txt[1:], loan=True)
        return cls(form=txt, loan=False)

    def __str__(self):
        return '%' + self.form if self.loan else self.form


@dataclasses.dataclass
class Synset:
    meaning_id: int
    meaning: str
    words: list[Word]
    comment: Optional[str]

    def __post_init__(self):
        self.meaning_id = int(self.meaning_id)
        assert self.meaning_id in MEANINGS_ALL

    @classmethod
    def from_txt(cls, line):
        header, body = line.split('\t', 1)
        body = body.strip()
        comment = ''
        if re.search('  | //', body):
            body, comment = re.split('  | //', body, maxsplit=1)
        # Degenerate cases:
        elif re.fullmatch(r'[^/]+/\s*[^/]+/$', body):
            body, comment, _ = body.split('/')
            body = body.strip()
        elif body.endswith('//'):  # pragma: no cover
            body = body[:-2].strip()
        elif body.endswith('/'):  # pragma: no cover
            body = body[:-1].strip()
        comment = comment.strip()
        words = []
        for word in body.split(','):
            word = word.strip()
            if word and word != MISSING_WORD:
                try:
                    words.append(Word.from_txt(word))
                except AssertionError:
                    logging.getLogger(__name__).warning('skipping invalid word "{}"'.format(word))

        number, meaning = header.split(maxsplit=1)
        if number.endswith('.'):
            number = number[:-1].strip()
        return cls(int(number), meaning.strip(), words, comment or None)

    @staticmethod
    def format(mid, meaning=None, form=MISSING_WORD, comment=None):
        return '{} {}\t{} //{}'.format(
            mid, meaning or MEANINGS_ALL[mid], form, ' ' + comment if comment else '')

    def format_words(self):
        return ', '.join(str(w) for w in self.words) or MISSING_WORD

    def __str__(self):
        return self.format(
            self.meaning_id,
            meaning=self.meaning,
            form=', '.join(str(w) for w in self.words),
            comment=self.comment)


def txt_header(synonyms=2, words=28, year=1700):
    """
     2    28  1700     3
(I4,20X,10A1)
    """
    def rjust(n, s=6):
        return str(n).rjust(s)

    lines = [
        '%s%s%s%s%s%s' % tuple(map(rjust, (synonyms, words, year, 3, 92, 72))), '(I4,20X,10A1)']

    for mid, concept in sorted(MEANINGS_ALL.items(), key=lambda p: p[0]):
        lines.append('%s%s%s' % (rjust(mid, 4), 20 * ' ', concept))

    lines.append('')
    for char in ASJPCODES:
        lines.append(char)
    lines.append('')
    lines.append('')
    return '\n'.join(lines)


@dataclasses.dataclass
class Doculect:
    id: str
    name: str
    classification_wals: Optional[str]
    classification_ethnologue: Optional[str]
    classification_glottolog: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    number_of_speakers: int
    recently_extinct: bool
    long_extinct: bool
    year_of_extinction: Optional[int]
    code_wals: Optional[str]
    code_iso: Optional[str]
    synsets: list[Synset]

    def __post_init__(self):
        self.synsets = [vv for vv in self.synsets if vv.words]
        if self.latitude is not None and self.longitude is not None:
            assert -90.0 <= self.latitude <= 90.0
            assert -180.0 <= self.longitude <= 180.0

    def get(self, item):
        for ss in self.synsets:
            if ss.meaning_id == item or ss.meaning == item or MEANINGS_ALL[ss.meaning_id] == item:
                return ss

    @property
    def asjp_name(self):
        name = self.name
        if '"' in name:
            name = name.split('"')[1]
        return name.replace("'", "").replace(" ", "_").replace("/", "_").upper()

    @property
    def wals_family(self):
        return self.classification_wals.split('.')[0] if self.classification_wals else None

    @property
    def wals_genus(self):
        return self.classification_wals.split('.')[1] if self.classification_wals else None

    @classmethod
    def from_txt(cls, txt, **kw):
        """
        The second line gives properties of the languages, in fixed format separated by blanks
        (not tabs), so the columns are important.

        Col. 2: 3 if the language is the first one in a new WALS family, 2 if it’s the first
        language in a new WALS genus, 1 otherwise.

        Col. 4-10, right justified: latitude in degrees and
        hundredths of a degree; minus means South.

        Col. 12-18, right justified: longitude in degrees a
        nd hundredths of a degree; minus means West.
        Latitudes and longitudes were ascertained from WALS, or from the maps in Ethnologue or
        Moseley and Asher (1994), or from information in the source for the list.

        Col. 19-30, right justified: number of speakers, from Ethnologue. This number always
        refers to the entire language, as defined in Ethnologue, even if the list itself
        refers to a dialect. The number is

            0 if the number of speakers is unknown;
            -1 if the language is recently extinct;
            -2 if the language is long extinct;
            or if the approximate date of extinction is known, the date is preceded by a minus
            sign.

        In the ASJP software, if there is a date in the first line of the entire file, lists
        with earlier extinction dates here are ignored, as are lists with -2; otherwise, all
        lists are read.

        Col. 34-36: three-letter WALS code, if any.

        Col. 40-42: three-letter ISO639-3 code, if any. This code is included for languages in
        previous editions of Ethnologue even if they aren’t in the 17th edition. Languages
        that lack an ISO639-3 code but can be placed in the Ethnologue classification are
        given a code consisting of two letters followed by the number 0 (for use in ASJP
        software).
        """
        lines = nfilter(txt.split('\n'))
        m = LANGUAGE_LINE_PATTERN.match(lines[0])
        assert m
        line = lines[1]
        try:
            lat = line[4:11].strip()
            lng = line[11:18].strip()
            nos = int(line[18:30].strip() or 0)
            code_wals = line[33:36].strip() or None
            code_iso = line[39:42].strip() or None
        except ValueError:  # pragma: no cover
            _, lat, lng, nos, code_wals, code_iso = line.strip().split()
            nos = int(nos)
        assert all(('\t' in line) or (not line.strip()) for line in lines[2:])
        words = [line for line in lines[2:] if '\t' in line]
        synsets = collections.OrderedDict()
        for line in words:
            synset = Synset.from_txt(line)
            assert synset.meaning_id not in synsets, '{}: {}'.format(m.group('name'), line)
            synsets[synset.meaning_id] = synset
        return cls(
            id=m.group('name'),
            name=' '.join(s.capitalize() for s in m.group('name').split('_')),
            classification_wals=m.group('w') if m.group('w') else None,
            classification_ethnologue=m .group('e') if m.group('e') else None,
            classification_glottolog=m.group('g') if m.group('g') else None,
            latitude=float(lat) if lat else None,
            longitude=float(lng) if lng else None,
            number_of_speakers=nos if nos >= 0 else 0,
            recently_extinct=nos == -1 or nos < -2,
            long_extinct=nos == -2,
            year_of_extinction=abs(nos) if nos < -2 else None,
            code_wals=code_wals,
            code_iso=code_iso,
            synsets=list(synsets.values()),
        )

    def __str__(self):
        return self.to_txt()

    def format(self, what):
        val = getattr(self, what)
        if what in ['latitude', 'longitude'] and val is not None:
            return '{:.2f}'.format(getattr(self, what))
        if what == 'number_of_speakers':
            if self.year_of_extinction:
                val = -self.year_of_extinction
            elif self.recently_extinct:
                val = -1
            elif self.long_extinct:
                val = -2
            return str(val)
        return val or ''

    def to_txt(self, add_missing=False, full_list=False, wals_marker='1'):
        """render the wordlist in the ASJP plain text format.
        """
        lines = [
            '%s{%s|%s@%s}' % (
                self.id,
                self.format('classification_wals'),
                self.format('classification_ethnologue'),
                self.format('classification_glottolog')),
            '%s%s%s%s%s%s' % (
                wals_marker.rjust(2),
                self.format('latitude').rjust(8),
                self.format('longitude').rjust(8),
                self.format('number_of_speakers').rjust(12),
                (self.code_wals or '').rjust(6),
                (self.code_iso or '').rjust(6))]
        synsets = {s.meaning_id: s for s in self.synsets}
        for mid, concept in sorted(MEANINGS_ALL.items(), key=lambda i: i[0]):
            if mid in synsets:
                lines.append(str(synsets[mid]))
            elif add_missing and ((mid in MEANINGS) or full_list):
                lines.append(Synset.format(mid))
        return '\n'.join(lines)

    @staticmethod
    def formatted_header():
        res = ['names', 'wls_fam', 'wls_gen', 'e', 'hh', 'lat', 'lon', 'pop', 'wcode', 'iso']
        return res + [v for _, v in sorted(MEANINGS_ALL.items(), key=lambda i: i[0])]

    def to_formatted_row(self):
        res = [
            self.id,
            self.wals_family,
            self.wals_genus,
            self.classification_ethnologue,
            self.classification_glottolog,
            self.format('latitude'),
            self.format('longitude'),
            self.format('number_of_speakers'),
            self.code_wals or '',
            self.code_iso or '',
        ]
        synsets = {s.meaning_id: s for s in self.synsets}
        for mid in sorted(MEANINGS_ALL.keys()):
            res.append(synsets[mid].format_words() if mid in synsets else MISSING_WORD)
        return res
