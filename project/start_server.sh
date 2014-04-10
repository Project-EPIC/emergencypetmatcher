#!bin/sh

gunicorn -D --bind 0.0.0.0:8000 project.wsgi:application --access-logfile logs/access.log --log-level DEBUG --error-logfile logs/error.log