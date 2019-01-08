#!/bin/bash -e
#
# Install Snowflake Python Connector
#
set -o pipefail
pip install -U virtualenv
python -m virtualenv venv
source ./venv/bin/activate
pip install numpy
pip install pytest pytest-cov pytest-rerunfailures
if [[ "$TRAVIS_PYTHON_VERSION" == "2.7" ]]; then
    pip install mock
fi
pip install .
pip list --format=columns
