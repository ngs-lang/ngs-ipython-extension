# ngs-ipython-extension
iPython extension for [ngs](https://github.com/ngs-lang/ngs) language

# Installation
## on local iPython or Jupyter Notebook
copy: `cp -v ngs.py $(ipython locate)/extensions/ngs.py`

or link: `ln -s $(pwd)/ngs.py $(ipython locate)/extensions/ngs.py`


## on Google Colab or other external Notebooks
Requirements
* For linux, `git`, `curl` and `apt` need to be installed
* For Mac: `git`, `curl` and `brew` need to be installed


Add the following lines to the notebook and run:

`!curl -o ngs-install.sh https://raw.githubusercontent.com/ngs-lang/ngs-ipython-extension/master/ngs-install.sh && chmod +x ngs-install.sh && ./ngs-install.sh`

`%load_ext ngs`


# Usage
This extension can be used both with Jupyter notebooks or ipython

## Loading extension
%load_ext ngs

## Re-loading extension
%reload_ext ngs

## Running
%ngs [single line expression]

%%ngs [multi line code]

## Handling of variables
Python defined variables will be sent to ngs context and can be used inside the scripts

On the return from ngs, the python context will be updated with the newer values
