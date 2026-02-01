#!/bin/sh
set -e

if [ "$DATABASE_ENGINE" = "django.db.backends.postgresql" ] || [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for PostgreSQL at ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."
  python - <<'PY'
import os, time
import psycopg2

host = os.getenv("POSTGRES_HOST", "db")
port = int(os.getenv("POSTGRES_PORT", "5432"))
dbname = os.getenv("POSTGRES_DB", "fitness_tracker")
user = os.getenv("POSTGRES_USER", "fitness_tracker")
password = os.getenv("POSTGRES_PASSWORD", "fitness_tracker")

max_tries = 60
for i in range(1, max_tries + 1):
    try:
        conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
        conn.close()
        print("PostgreSQL is available.")
        break
    except Exception as e:
        if i == max_tries:
            raise
        time.sleep(1)
PY
fi

python manage.py migrate --noinput

python manage.py collectstatic --noinput || true

exec "$@"
