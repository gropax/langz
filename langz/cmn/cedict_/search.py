# -*- coding: utf-8 -*-

import sys
import os
import re
import sqlite3
import cedict


CONF_DIR = os.path.expanduser('~/.langz/cmn')
DB_PATH = os.path.join(CONF_DIR, 'cedict.db')
FIELDS_INDEX = {'t': 0, 's': 1, 'p': 2, 'd':3}

class CedictSearchCommand:
    def __init__(self, args):
        self.args = args

    def execute(self):
        self.check_db()

        search = self.search_proc()
        format = self.format_proc()

        for s in self.args.infile:
            q = s.strip().decode('utf-8')

            rets = search(q)
            out = "\n".join(format(ret) for ret in rets) + "\n"

            self.args.outfile.write(out.encode('utf-8'))

    def search_proc(self):
        if self.args.character:
            return self.search_char
        elif self.args.pinyin:
            return self.search_pinyin
        else:
            raise NotImplemented("Search CEDICT by definition")
            #return self.search_definition

    def search_char(self, char):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM entries \
                        WHERE traditional=? OR simplified=?', (char, char))
        return cursor.fetchall()

    def search_pinyin(self, pinyin):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        nb_pinyin = cedict.depinyinize(pinyin)
        cursor.execute('SELECT * FROM entries WHERE pinyin=?', (nb_pinyin,))

        return cursor.fetchall()

    def format_proc(self):
        f = self.args.fields
        s = "\t".join(re.sub('\w', '%s ', c).rstrip() for c in f.split())
        ix = [ FIELDS_INDEX[i] for i in list(f.replace(' ', '')) ]
        return lambda t: s % tuple(t[i] for i in ix)

    def check_db(self):
        if not os.path.isfile(DB_PATH):
            sys.stderr.write(
                "The CEDICT database doesn't exist yet. To create it:\n\n"\
                "    $ cmn cedict setup ./path/to/cedict.txt\n\n")
            exit(1)
