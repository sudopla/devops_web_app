#!/bin/bash

nginx
/usr/bin/env gunicorn --chdir /usr/src/app/ devops_project.wsgi:application --timeout 120 --bind 0.0.0.0:8080 --workers 3
