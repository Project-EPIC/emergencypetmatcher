#!bin/bash
printf "[START]: Virtualizing..."
source bin/activate
export DJANGO_SETTINGS_MODULE="project.settings"
printf "OK\n"

if [ "$1" == -prod ]; then
	echo "[START]: Starting Gunicorn Server, will hang here..."
	gunicorn --bind 0.0.0.0:8889 project.wsgi:application --access-logfile logs/access.log --error-logfile logs/error.log
	echo "[OK]: Done."	
else
	echo "[START]: Starting Django Development Server..."
	python manage.py runserver 0.0.0.0:8000
	echo "[OK]: Done."	
fi 
