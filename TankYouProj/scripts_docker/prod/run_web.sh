#!/bin/sh

# -------------------------------------
# Migraciones
# -------------------------------------
python manage.py migrate --noinput

# -------------------------------------
# Static (IMPORTANTE para Nginx)
# -------------------------------------
python manage.py collectstatic --noinput

# -------------------------------------
# Iniciar Gunicorn
# -------------------------------------
exec gunicorn TankYou.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
