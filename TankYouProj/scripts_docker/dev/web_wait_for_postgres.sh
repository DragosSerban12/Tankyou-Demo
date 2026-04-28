#!/bin/sh

echo "Esperando a Postgres..."

until python -c "
import psycopg2, os, sys

def read_secret(name):
    path = f'/run/secrets/{name}'
    if not os.path.exists(path):
        sys.exit(1)
    with open(path) as f:
        return f.read().strip()

try:
    psycopg2.connect(
        dbname=read_secret('POSTGRES_DB'),
        user=read_secret('POSTGRES_USER'),
        password=read_secret('POSTGRES_PASSWORD'),
        host='db',
        port=5432,
    )
except Exception:
    sys.exit(1)

sys.exit(0)
"
do
  echo "Postgres no disponible - esperando..."
  sleep 1
done

echo "Postgres listo - arrancando Django"
exec sh /code/scripts_docker/dev/run_web.sh
