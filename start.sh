set -e

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

gunicorn blogApp.wsgi:application --bind 0.0.0.0:8000
