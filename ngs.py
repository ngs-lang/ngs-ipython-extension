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
from subprocess import Popen, PIPE

from IPython import get_ipython
from IPython.core.magic import (magics_class, line_cell_magic, Magics)
from ipywidgets import FloatProgress, HTML, VBox
from IPython.display import display

ngs_process = Popen(["ngs-jupyter-connector.ngs"], stdout=PIPE, stdin=PIPE, shell=True)

@magics_class
class NGSMagics(Magics):

    def __init__(self, *args, **kwargs):
        self.displayed_widgets = {}
        return super().__init__(*args, **kwargs)

    def ensure_displayed(self, widget):
        if widget.model_id in self.displayed_widgets:
            return
        display(widget)
        self.displayed_widgets[widget.model_id] = True

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

        output_pfx = {
            1: "",
            'warn': "\x1b[33mWARNING: ",
            'error': "\x1b[1;31m\n",
            'exc': "\x1b[31m\n",
        }

        status_widget = HTML()
        progress_widget = FloatProgress(min=0, max=1, value=0)
        # vbox_widget = VBox()

        status_widget.value = 'aaa'

        ret = None
        while True:
            # Read ngs response
            result = ngs_process.stdout.readline()

            # Parse json response
            result_json = json.loads(result)
            t = result_json['type']

            if t == 'finish':
                break

            if t == 'output':
                print(result_json['channel'])

                pfx = output_pfx[result_json['channel']]
                print(pfx + result_json['text'] + "\x1b[0m")
                continue

            if t == 'var':
                ip.user_ns[result_json['name']] = result_json['value']
                continue

            if t == 'result':
                ret = result_json['value']
                continue

            if t == 'error':
                progress_widget.bar_style = 'danger'
                for line in result_json['text_lines']:
                    print("\x1b[31m" + line + "\x1b[0m")
                continue

            if t == 'status':
                self.ensure_displayed(status_widget)
                status_widget.value = result_json['text']
                continue

            if t == 'progress':
                self.ensure_displayed(progress_widget)
                progress_widget.value = result_json['value'][0]
                progress_widget.max = result_json['value'][1]
                continue

            print("*** WARNING: Unknown message type from NGS: " + t)

        status_widget.close()
        progress_widget.close()
        return ret

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
