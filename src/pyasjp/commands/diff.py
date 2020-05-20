"""
Diff synsets between two ASJP releases.
"""
import collections

from clldutils.clilib import PathType

from pyasjp import ASJP
from pyasjp.meanings import MEANINGS, MEANINGS_NON_CORE


def register(parser):
    parser.add_argument(
        'listA',
        type=PathType(type='file')
    )
    parser.add_argument(
        'listB',
        type=PathType(type='file')
    )
    parser.add_argument(
        '--match-label',
        help="Match synsets based on meaning label rather than meaning number",
        action='store_true',
        default=False,
    )


def run(args):
    api = ASJP('.')
    reverse_meaning_lookup = {}
    for mid, ms in MEANINGS.items():
        for m in ms:
            reverse_meaning_lookup[m] = mid
    for mid, m in MEANINGS_NON_CORE.items():
        reverse_meaning_lookup[m] = mid

    formsA = collections.defaultdict(lambda: collections.defaultdict(dict))
    for dl in api.iter_doculects(args.listA):
        for ss in dl.synsets:
            mid = reverse_meaning_lookup[ss.meaning] if args.match_label else ss.meaning_id
            formsA[dl.id][mid] = ', '.join(str(w) for w in ss.words)

    for dl in api.iter_doculects(args.listB):
        if dl.id in formsA:
            for ss in dl.synsets:
                mid = reverse_meaning_lookup[ss.meaning] if args.match_label else ss.meaning_id
                if mid in formsA[dl.id]:
                    formsB = ', '.join(str(w) for w in ss.words)
                    formsetB = set(
                        w.strip().replace('~', '') for w in formsB.split(','))
                    formsetA = set(
                        w.strip().replace('~', '') for w in formsA[dl.id][mid].split(','))
                    # if formsA[dl.id][mid] != formsB:
                    if formsetA != formsetB:
                        print('{}:{}:{} -> {}'.format(dl.id, mid, formsA[dl.id][mid], formsB))
