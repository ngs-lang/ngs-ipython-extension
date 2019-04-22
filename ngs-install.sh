#!/bin/bash

# install ngs
if [ ! -d 'ngs' ]
then
    git clone --single-branch --branch dev https://github.com/ngs-lang/ngs.git
    cd ngs
    if [ $(uname -s) == 'Darwin' ]
    then
        ./install-mac.sh
    else
        ./install-linux.sh
    fi
fi

# copy ngs ipython extension
curl -o $(ipython locate)/extensions/ngs.py https://raw.githubusercontent.com/ngs-lang/ngs-ipython-extension/master/ngs.py

echo "DONE. Please run %reload_ext ngs"