import sys
from argparse import ArgumentParser, FileType


def arg_parser(parser=None):
    parser = parser or ArgumentParser(description="Tools for Mandarin dictionary research and\
               pinyin manipulation")

    subparsers = parser.add_subparsers(dest="command")

    # Pinyin Command
    parser_pinyin = subparsers.add_parser('pinyin', help="Pinyin conversions")
    parser_pinyin.add_argument('infile', nargs='?', type=FileType('r'),
                            default=sys.stdin)
    parser_pinyin.add_argument('-o', '--outfile', nargs='?', type=FileType('w'),
                            default=sys.stdout)
    group = parser_pinyin.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--accent', action="store_true")
    group.add_argument('-n', '--number', action="store_true")
    group.add_argument('-r', '--remove', action="store_true")

    # Cedict Command
    parser_cedict = subparsers.add_parser('cedict', help="Search in CeDict")
    cedict_subparsers = parser_cedict.add_subparsers(dest="subcommand")

    # Cedict Search Subcommand
    search_parser = cedict_subparsers.add_parser('search', help="Search in CEDICT")
    search_parser.add_argument('infile', nargs='?', type=FileType('r'),
                            default=sys.stdin)
    search_parser.add_argument('-o', '--outfile', nargs='?', type=FileType('w'),
                            default=sys.stdout)
    search_parser.add_argument('-q', '--query', action="store")
    search_parser.add_argument('-f', '--fields', action="store", default="stpd")

    group = search_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--pinyin', action="store_true")
    group.add_argument('-c', '--character', action="store_true")
    group.add_argument('-d', '--definition', action="store_true")

    # Cedict Setup Subcommand
    setup_parser = cedict_subparsers.add_parser('setup', help="Setup CEDICT database")
    setup_parser.add_argument('infile', type=FileType('r'),
                              help="The CEDICT dictionary text file")
    setup_parser.add_argument('-f', '--force', action="store_true")


    return parser
