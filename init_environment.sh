#!/bin/bash
# Create if not exist
if [[ ! -e venv ]]; then virtualenv -p /usr/bin/python3 venv; fi
source ./venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=$(pwd)
