# ngs-ipython-extension
iPython extension for ngs language

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
