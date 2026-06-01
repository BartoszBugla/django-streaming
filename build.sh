#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Zainstaluj i zbuduj TailwindCSS
python manage.py tailwind install --no-input
python manage.py tailwind build --no-input

# Skompiluj pliki statyczne
python manage.py collectstatic --no-input

# Uruchom migracje bazy danych
python manage.py migrate
