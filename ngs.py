# ngs.py
"""Extension for integration with ngs language of IPython notebooks
Usage:
%load_ext ngs

# single line:
%ngs echo('hello')
# multiline:
%ngs echo('hello')
...  echo('word')
...
...
"""

from IPython.core.magic import (magics_class, line_cell_magic, Magics)
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

        exc = ""
        for dest in json_result['output']:
            if dest[0] == 'warn':
                print("\x1b[33mWARNING:", dest[1], "\x1b[0m")
            if dest[0] == 'exc':
                exc = exc + dest[1] + '\n'
            if dest[0] == 1:
                print(dest[1])

        if exc:
            print("\x1b[31m" + exc + "\x1b[0m")

        if 'result' in json_result:
            return json_result['result']


def load_ipython_extension(ipython):
    print('loading ngs module')
    ngs_magics = NGSMagics(ipython)
    ipython.register_magics(ngs_magics)

def unload_ipython_extension(ipython):
    print('unloading ngs module')
    ngs_process.stdin.close()  # for ngs to finish gracefully
    ngs_process.wait()
