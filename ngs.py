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

__version__ = '0.0.1'

import json
from IPython import get_ipython
from IPython.core.magic import (magics_class, line_cell_magic, Magics)
from subprocess import Popen, PIPE


ngs_process = Popen(["ngs-jupyter-connector.ngs"], stdout=PIPE, stdin=PIPE, shell=True)

@magics_class
class NGSMagics(Magics):

    @line_cell_magic
    def ngs(self, line, cell=None):

        # Prepare input
        called_with = line.strip()
        if cell is not None:  # multi-line mode
            called_with = called_with + "\n" + cell.strip()

        # Prepare json input
        ip = get_ipython()
        input_vars = {}
        for var in ip.run_line_magic('who_ls', ''):
            input_vars[var] = ip.user_ns[var]
        input_json = json.dumps({"vars": input_vars, "expr": called_with})
        # print('sending:', input_json)

        # Send input to ngs
        ngs_process.stdin.write(bytes(input_json + '\n', 'utf-8'))
        ngs_process.stdin.flush()

        # Read ngs response
        result = ngs_process.stdout.readline()

        # Parse json response
        result_json = json.loads(result)
        result_exception = ""
        if 'output' in result_json:
            for output in result_json['output']:
                if output[0] == 'warn':  # warnings
                    print("\x1b[33mWARNING:", output[1], "\x1b[0m")

                if output[0] == 'exc':  # exceptions
                    result_exception = result_exception + output[1] + '\n'

                if output[0] == 1:  # normal output
                    print(output[1])

        if 'vars' in result_json:
            result_vars = result_json['vars']
            for key in result_vars:
                if ip.user_ns[key] != result_vars[key]:
                    ip.user_ns[key] = result_vars[key]

        if 'error' in result_json:
            print("\x1b[1;31m" + '\n'.join(result_json['error']['text']) + "\x1b[0m")
        if result_exception:
            print("\x1b[31m" + "\n" + result_exception + "\x1b[0m")

        if 'result' in result_json:
            return result_json['result']


def load_ipython_extension(ipython):
    print('loading ngs module\n')
    ngs_magics = NGSMagics(ipython)
    ipython.register_magics(ngs_magics)
    print('usage: %ngs [command]')
    print('       %%ngs [multi-line code]')

def unload_ipython_extension(ipython):
    print('unloading ngs module')
    ngs_process.stdin.close()  # for ngs to finish gracefully
    ngs_process.wait()
