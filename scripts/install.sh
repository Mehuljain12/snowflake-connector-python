#!/bin/bash -e
#
# Install Snowflake Python Connector
#
set -o pipefail
source ./venv/bin/activate
pip install numpy
pip install pytest pytest-cov pytest-rerunfailures
if [[ "$TRAVIS_PYTHON_VERSION" == "2.7" ]] || [[ $PYTHON_VERSION == "2.7"* ]]; then
    pip install mock
fi
pip install .
pip list --format=columns
