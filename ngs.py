# ngs.py

from IPython.core.magic import (magics_class, line_cell_magic, Magics)
from IPython.core.error import UsageError
from subprocess import Popen, PIPE, STDOUT
import json

__version__ = '0.0.1'

ngs_process = Popen(["ngs-jupyter-connector.ngs"], stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)

@magics_class
class NGSMagics(Magics):

    @line_cell_magic
    def ngs(self, line, cell=None):

        if cell is None:
            called_with = line.strip()
        else:
            called_with = line.strip() + "\n" + cell.strip()

        json_input = json.dumps({"vars": {}, "expr": called_with})
        print(json_input)

        grep_stdout = ngs_process.communicate(input=bytes(json_input, 'utf-8'))[0]
        return grep_stdout.decode('utf-8').strip()


def load_ipython_extension(ipython):
    ngs_magics = NGSMagics(ipython)
    ipython.register_magics(ngs_magics)

def unload_ipython_extension(ipython):
    ngs_process.stdin.close()
