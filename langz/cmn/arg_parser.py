# -*- coding: utf-8 -*-

import sys
from argparse import ArgumentParser, FileType


def arg_parser(parser=None):
    parser = parser or ArgumentParser(
        prog="cmn",
        description="Tools for Mandarin dictionary research and pinyin manipulation"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Cedict Command
    parser_cedict = subparsers.add_parser('cedict',
        help="Search in CC-CEDICT Mandarin-English dictionary",
        description="Search in CC-CEDICT Mandarin-English dictionary.",
        epilog="NOTE: To search the CC-CEDICT dictionary, you must first setup"\
               "the database. Download the CC-CEDICT file and run "\
               "`$ cmn cedict setup cedict.txt`.")

    cedict_subparsers = parser_cedict.add_subparsers(dest="subcommand")

    # Cedict Search Subcommand
    search_parser = cedict_subparsers.add_parser('search',
        help="Search dictionary")
    search_parser.add_argument('infile', nargs='?', type=FileType('r'),
                            default=sys.stdin)
    search_parser.add_argument('-o', '--outfile', nargs='?', type=FileType('w'),
                            default=sys.stdout)
    search_parser.add_argument('-q', '--query', action="store")
    search_parser.add_argument('-f', '--fields', action="store", default="stpd")

    group = search_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--pinyin', action="store_true")
    group.add_argument('-c', '--character', action="store_true")
    #group.add_argument('-d', '--definition', action="store_true")

    # Cedict Setup Subcommand
    setup_parser = cedict_subparsers.add_parser('setup',
        help="Setup database")
    setup_parser.add_argument('infile', type=FileType('r'),
                              help="The CEDICT dictionary text file")
    setup_parser.add_argument('-f', '--force', action="store_true")

    # Pinyin Command
    parser_pinyin = subparsers.add_parser('pinyin',
        help=u"Conversion between pinyin format (ex: ni3hao3, nǐhǎo)")
    parser_pinyin.add_argument('infile', nargs='?', type=FileType('r'),
                            default=sys.stdin)
    parser_pinyin.add_argument('-o', '--outfile', nargs='?', type=FileType('w'),
                            default=sys.stdout)
    group = parser_pinyin.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--accent', action="store_true")
    group.add_argument('-n', '--number', action="store_true")
    group.add_argument('-r', '--remove', action="store_true")


    return parser
