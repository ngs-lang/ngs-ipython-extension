#!/bin/bash

# install ngs
if ! command -v ngs &> /dev/null
then
    echo "NGS not found, installing ngs"
    curl https://ngs-lang.org/install.sh | bash
fi

# copy ngs ipython extension
curl -o $(ipython locate)/extensions/ngs.py https://raw.githubusercontent.com/ngs-lang/ngs-ipython-extension/master/ngs.py

echo "DONE. Please run %reload_ext ngs"