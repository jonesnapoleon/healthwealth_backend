#!/bin/sh

/code/manage.py migrate
/code/manage.py collectstatic 
/code/manage.py rqworker &
gunicorn --pythonpath backend main.wsgi --bind 0.0.0.0:8000