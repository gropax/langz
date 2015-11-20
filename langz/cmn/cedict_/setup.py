# -*- coding: utf-8 -*-

import sys
import os
import cedict
import sqlite3

CONF_DIR = os.path.expanduser('~/.langz/cmn')
DB_PATH = os.path.join(CONF_DIR, 'cedict.db')

class CedictSetupCommand:
    def __init__(self, args):
        self.args = args

    def execute(self):
        if not self.db_exist() or self.args.force:
            self.remove_db()
            try:
                sys.stderr.write("Creating CC-CEDICT database... ")
                self.setup_db()
                sys.stderr.write("DONE\n")
            except:
                sys.stderr.write("An error occured")
                self.remove_db()
                exit(1)

    def db_exist(self):
        return os.path.isfile(DB_PATH)

    def remove_db(self):
        if os.path.isfile(DB_PATH):
            os.remove(DB_PATH)

    def create_conf_dir(self):
        if not os.path.isdir(CONF_DIR):
            os.makedirs(CONF_DIR)

    def setup_db(self):
        self.create_conf_dir()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create table
        cursor.execute('''CREATE TABLE entries (traditional text,
                                                simplified text,
                                                pinyin text,
                                                definitions text,
                                                variants text,
                                                measure_word text)''')

        for ch, chs, py, ds, vs, mws in cedict.iter_cedict(self.args.infile):
            _py = py.replace(' ', '')
            _ds = "|".join(ds)
            _vs = "|".join([k + ":" + v for d in vs for k, v in d.items()])
            _mws = "|".join([";".join(mw) for mw in mws])
            entry = (ch, chs, _py, _ds, _vs, _mws)
            cursor.execute("INSERT INTO entries VALUES (?,?,?,?,?,?)", entry)

        conn.commit()
        conn.close()
