#!/bin/bash
set -e

apt-get update
apt-get install -y libsqlite3-dev || true 

# Проверка и установка pip, если он отсутствует
if ! command -v pip &> /dev/null
then
    echo "pip не найден. Устанавливаю pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
fi

python3 -m pip install -r requirements.txt

python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate

gunicorn blogApp.wsgi:application --bind 0.0.0.0:8000
