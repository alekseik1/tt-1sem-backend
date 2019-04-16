#!/bin/bash
flask db upgrade
exec gunicorn -b :5000 --access-logfile access.log --error-logfile error.log run:app
