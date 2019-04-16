#!/bin/bash
# Create if not exist
if [[ ! -e venv ]]; then virtualenv -p /usr/bin/python3 venv; fi
source ./venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=$(pwd)/
# Workaround for Cursor error (see https://www.elastic.co/guide/en/elasticsearch/client/curator/current/faq_unicode.html)
export LC_ALL=C.UTF-8
