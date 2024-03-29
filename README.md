# ngs-ipython-extension
iPython extension for [ngs](https://github.com/ngs-lang/ngs) language

# Installation
## on local iPython or Jupyter Notebook
copy: `cp -v ngs.py $(ipython locate)/extensions/ngs.py`

or link: `ln -s $(pwd)/ngs.py $(ipython locate)/extensions/ngs.py`

## using Docker

```
docker run -p 8888:8888 ngslang/ngs-jupyter
```

Then access the http://127.0.0.1:8888/?token=XXXXX  that appears in the output

## using Docker - local build

Build:
`make docker-build`

Run:
`make docker-run`

Then access the http://127.0.0.1:8888/?token=XXXXX  that appears in the output

## on Google Colab or other external Jupyter Notebooks
Requirements
* For linux, `git`, `curl` and `apt` need to be installed
* For Mac: `git`, `curl` and `brew` need to be installed


Add the following lines to the notebook and run:

`!curl https://raw.githubusercontent.com/ngs-lang/ngs-ipython-extension/master/ngs-install.sh | bash`

# Usage
This extension can be used both with Jupyter Notebooks or iPython

## Loading extension
`%load_ext ngs`

## Re-loading extension
`%reload_ext ngs`

## Running
`%ngs [single line expression]`

`%%ngs [multi line code]`

## Handling of variables
Python defined variables will be sent to ngs context and can be used inside the scripts

On the return from ngs, the Python context will be updated with the newer values
