# ngs.py

from IPython.core.magic import (magics_class, line_cell_magic, Magics)
from IPython.core.error import UsageError
from subprocess import Popen, PIPE
import json

__version__ = '0.0.1'

ngs_process = Popen(["ngs-jupyter-connector.ngs"], stdout=PIPE, stdin=PIPE, shell=True)

@magics_class
class NGSMagics(Magics):

    @line_cell_magic
    def ngs(self, line, cell=None):

        if cell is None:
            called_with = line.strip()
        else:
            called_with = line.strip() + "\n" + cell.strip()

        json_input = json.dumps({"vars": {}, "expr": called_with})
        print('sending:', json_input)

        ngs_process.stdin.write(bytes(json_input + '\n', 'utf-8'))
        ngs_process.stdin.flush()
        result = ngs_process.stdout.readline()
        json_result = json.loads(result)

        return json_result['result']

def load_ipython_extension(ipython):
    print('loading ngs module')
    ngs_magics = NGSMagics(ipython)
    ipython.register_magics(ngs_magics)

def unload_ipython_extension(ipython):
    print('unloading ngs module')
    ngs_process.stdin.close()  # for ngs to finish gracefully
    ngs_process.wait()
