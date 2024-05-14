#/bin/bash

PYTHON_VERSION=3.12.2

pyenv install $PYTHON_VERSION
cat .python-version | xargs -I python-version pyenv virtualenv $PYTHON_VERSION python-version
cat .python-version | pyenv activate
pip install -r requirements.txt
