python manage.py makemigrations
python manage.py migrate 
python manage.py collectstatic --noinput
gunicorn blogApp.wsgi:application --bind 0.0.0.0:8001 --workers 4