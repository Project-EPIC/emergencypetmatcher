#!bin/bash
printf "[START]: Virtualizing..."
source bin/activate
printf "OK\n"

if [ "$1" == -prod ]; then
	echo "[START]: Starting Gunicorn Server..."
	sudo gunicorn -D --bind 0.0.0.0:8000 project.wsgi:application --access-logfile logs/access.log --error-logfile logs/error.log
	echo "[OK]: Done."	
else
	echo "[START]: Starting Django Development Server..."
	sudo python manage.py runserver 0.0.0.0:80
	echo "[OK]: Done."	
fi 
