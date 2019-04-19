# ngs.py

from IPython.core.magic import (magics_class, line_cell_magic, Magics)
from IPython.core.error import UsageError
import subprocess

__version__ = '0.0.1'

@magics_class
class NGSMagics(Magics):

    @line_cell_magic
    def ngs(self, line, cell=None):
        line = line.strip()
        if cell is None:
            print("Called with [ line:", line, "]")
            rr = subprocess.run(['ngs', '{"vars": {}, "expr": "' + line + '" }'], stdout=subprocess.PIPE)
        else:
            cell = cell.strip()
            print("Called with [ line:", line, " cell:", cell, "]")
            rr = subprocess.run(['ngs', '{"vars": {}, "expr": "' + line + " " + cell + '" }'], stdout=subprocess.PIPE)

        return rr.stdout.decode('utf-8')


def load_ipython_extension(ipython):
    ngs_magics = NGSMagics(ipython)
    ipython.register_magics(ngs_magics)
