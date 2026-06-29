#!/bin/bash
set -e

export PATH="/nix/store/k28ypnisbhajg3x1kv5hy7h2vjbajkvy-replit-runtime-path/bin:$PATH"
export DATABASE_URL="postgresql+psycopg2://postgres@/walletdb?host=/run/postgresql"

PGDATA="/home/runner/pgdata"
SOCKET_DIR="/run/postgresql"

# Ensure socket dir exists
mkdir -p "$SOCKET_DIR"

# Initialize data dir if missing
if [ ! -f "$PGDATA/PG_VERSION" ]; then
  echo "[db] Initializing PostgreSQL data directory..."
  initdb -D "$PGDATA" --no-locale --encoding=UTF8 -U postgres
fi

# Start postgres if not already running
if ! pg_isready -h "$SOCKET_DIR" -p 5432 -q 2>/dev/null; then
  echo "[db] Starting PostgreSQL..."
  pg_ctl -D "$PGDATA" -l "$PGDATA/pg.log" -o "-p 5432 -k $SOCKET_DIR" start
  sleep 2
fi

# Create DB if missing
createdb -h "$SOCKET_DIR" -U postgres walletdb 2>/dev/null || true

# Run migrations
echo "[db] Running migrations..."
cd /home/runner/workspace
python -m alembic upgrade head

# Start API
echo "[api] Starting uvicorn..."
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
