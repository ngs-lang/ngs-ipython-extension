# ngs-ipython-extension
iPython extension for [ngs](https://github.com/ngs-lang/ngs) language

## Loading extension
%load_ext ngs

## Running connector
%ngs [single line expression]

%%ngs [multi line code]

## Handling of variables
Python defined variables will be sent to ngs context and can be used there
On the return from ngs, the python context will be updated

## Usages
Can be used both with Jupyter notebooks or ipython

## Install with local iPython or Jupyter Notebook
copy: `cp -v ngs.py $(ipython locate)/extensions/ngs.py`

or link: `ln -s $(pwd)/ngs.py $(ipython locate)/extensions/ngs.py`


## Install on Google Colab or other external Notebook Systems
Add the following lines to the notebook and run:

`!curl -o ngs-install.sh https://raw.githubusercontent.com/ngs-lang/ngs-ipython-extension/master/ngs-install.sh && chmod +x ngs-install.sh && ./ngs-install.sh`

`%load_ext ngs`