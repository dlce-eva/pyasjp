"""
Convert an ASJP database to tab-delimited "formatted" data.
"""
import csv

from clldutils.clilib import PathType
from csvw.dsv import UnicodeWriter

from pyasjp import ASJP


def register(parser):
    parser.add_argument('list', type=PathType())
    parser.add_argument('out', type=PathType(must_exist=False, type='file'))


def run(args):
    api = ASJP(args.list if args.list.is_dir() else '.')

    with UnicodeWriter(args.out, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar="") as w:
        for i, dl in enumerate(api.iter_doculects(args.list if args.list.is_file() else None)):
            if not i:
                w.writerow(dl.formatted_header())
            w.writerow(dl.to_formatted_row())
