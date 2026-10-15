#!/usr/bin/env bash
# Run on the Linux host, from anywhere:
#   bash deploy/prepare.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  echo "Copy .env.example to .env and set DEBUG=False before continuing."
  exit 1
fi

PY="${PYTHON:-python3}"
if [[ ! -d venv ]]; then
  "$PY" -m venv venv
fi
# shellcheck disable=SC1091
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
mkdir -p media staticfiles tmp
python manage.py migrate --noinput
python manage.py collectstatic --noinput
echo "Database migrated and static files collected."
echo "Create the admin user once: python manage.py createsuperuser"
