# -*- coding: utf-8 -*-

import sys
import os
import sqlite3
import cedict


class PinyinCommand:
    def __init__(self, args):
        self.args = args

    def io(self, proc):
        for s in self.args.infile:
            q = s.strip().decode('utf-8')
            out = proc(q) + "\n"
            self.args.outfile.write(out.encode('utf-8'))

    def execute(self):
        self.io(self.process())

    def process(self):
        if self.args.accent:
            return cedict.pinyinize
        elif self.args.number:
            return cedict.depinyinize
        else:
            return self.remove_tone_marks

    def remove_tone_marks(self, string):
        return u''.join([c for c in cedict.depinyinize(s)
                           if not c.isdigit()])
