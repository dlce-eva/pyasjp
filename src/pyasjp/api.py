import itertools
import collections

from clldutils.apilib import API
from clldutils.misc import lazyproperty
from csvw.dsv import reader

from pyasjp import models


def iter_chunks(fp):
    wordlist = None

    for line in fp:
        m = models.LANGUAGE_LINE_PATTERN.match(line)
        if m:
            if wordlist:
                yield wordlist
            wordlist = [line]
        else:
            if wordlist:
                wordlist.append(line)

    if wordlist:
        yield wordlist


class ASJP(API):
    def to_txt(self, *doculects, **kw):
        res = [models.txt_header()]
        wals_family, wals_genus = None, None
        for dl in sorted(doculects, key=lambda d: (d.wals_family or 'ZZZ', d.wals_genus or 'ZZZ')):
            if dl.wals_family and dl.wals_family != wals_family:
                wals_marker = '3'
            elif dl.wals_genus and dl.wals_genus != wals_genus:
                wals_marker = '2'
            else:
                wals_marker = '1'
            wals_family = dl.wals_family
            wals_genus = dl.wals_genus
            res.append(dl.to_txt(
                add_missing=kw.get('add_missing', False),
                full_list=kw.get('full_list', False),
                wals_marker=wals_marker))
        return '\n'.join(res) + '\n'

    def iter_doculects(self, p=None):
        ids = set()
        p = p or self.repos / 'lists.txt'
        with p.open(encoding='cp1252') as fp:
            for chunk in iter_chunks(fp):
                d = models.Doculect.from_txt('\n'.join(chunk))
                if d.id in ids:  # pragma: no cover
                    print('skipping duplicate doculect {}'.format(d.id))
                    continue
                ids.add(d.id)
                yield d

    @lazyproperty
    def sources(self):
        res = collections.defaultdict(list)
        for i, row in enumerate(
            reader(self.repos / 'sources.csv', dicts=True, encoding='cp1252'),
            start=1,
        ):
            res[row['ASJP_NAME'].lower().replace('-', '_')].append(models.Source(
                id=i, **{k.lower(): v for k, v in row.items()}))
        return res

    def source(self, dl):
        return self.sources.get(dl.asjp_name.lower())

    def transcriber(self, dl):
        srcs = self.source(dl)
        if srcs:
            return [
                self.transcribers[trs] for trs in
                set(itertools.chain(*[src.list_made_by for src in srcs]))]

    @lazyproperty
    def transcribers(self):
        return {
            t.id: t for t in
            [models.Transcriber(*row) for row in reader(self.repos / 'transcribers.csv')]}
