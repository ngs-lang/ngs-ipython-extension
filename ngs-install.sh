#!/bin/bash

# install ngs
if [ ! -d 'ngs' ]
then
    curl https://ngs-lang.org/install.sh | bash
fi

# copy ngs ipython extension
curl -o $(ipython locate)/extensions/ngs.py https://raw.githubusercontent.com/ngs-lang/ngs-ipython-extension/master/ngs.py

echo "DONE. Please run %reload_ext ngs"