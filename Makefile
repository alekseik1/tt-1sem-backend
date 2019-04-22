SHELL:=/bin/bash
ROOT:=$(shell pwd)
VENV=$(ROOT)/venv/bin
PIDFILE:=$(ROOT)/celery.pid
REQ_FILE:=$(ROOT)/requirements.txt
PYTHON_PATH:=/usr/bin/python3

environment:
	if [[ ! -e venv ]]; then virtualenv -p $(PYTHON_PATH) venv; fi
	$(VENV)/pip install -r $(REQ_FILE)

tests: environment celery
	PYTHONPATH=$(ROOT) $(VENV)/python tests/views_test.py

run: environment celery
	PYTHONPATH=$(ROOT) $(VENV)/gunicorn -b 0.0.0.0:5000 app:app

celery: environment
	$(VENV)/celery worker -A app.celery -l info -D --pidfile $(PIDFILE)

stop:
	PIDFILE=$(PIDFILE)
	if [ -e $(PIDFILE) ]; then kill $(shell cat $(PIDFILE)) &&  rm $(PIDFILE); fi

migrate_db: environment
	PYTHONPATH=$(ROOT) $(VENV)/python run.py db migrate_db

upgrade_db: migrate
	PYTHONPATH=$(ROOT) $(VENV)/python run.py db upgrade
