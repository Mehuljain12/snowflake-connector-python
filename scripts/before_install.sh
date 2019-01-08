#!/bin/bash -e
#
# before_install
#
set -o pipefail

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    brew update
    brew install openssl readline sqlite3 xz zlib
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    pyenv install ${PYTHON_VERSION}
    export PYENV_VERSION=$PYTHON
    export PATH="${HOME}/.pyenv/shims:${PATH}"
    if [[ $PYTHON_VERSION == "2.7"* ]]; then
        pip install -U virtualenv
        python -m virtualenv venv
    else
        python3 -m venv venv
    fi
else
    sudo apt-get update
    pip install -U virtualenv
    python -m virtualenv venv
fi
openssl aes-256-cbc -k "$super_secret_password" -in parameters.py.enc -out test/parameters.py -d
