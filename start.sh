set -e

pip install -r requirements.txt

python3 manage.py collectstatic
python3 manage.py makemigrations
python3 manage.py migrate

gunicorn blogApp.wsgi:application --bind 0.0.0.0:8000
