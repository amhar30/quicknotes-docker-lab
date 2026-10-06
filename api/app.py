"""QuickNotes API - a tiny Flask service backed by PostgreSQL and Redis.

Students do NOT need to change this file. Your job is to containerise it.
"""
import os
import socket
import time

import psycopg2
import redis
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "notes")
DB_USER = os.getenv("DB_USER", "notes")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
APP_VERSION = os.getenv("APP_VERSION", "dev")

cache = redis.Redis(host=REDIS_HOST, port=6379, socket_connect_timeout=2)


def get_db():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, connect_timeout=3)


def init_db(retries=10):
    for attempt in range(1, retries + 1):
        try:
            with get_db() as conn, conn.cursor() as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    text VARCHAR(280) NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW())""")
            print("Database ready", flush=True)
            return
        except psycopg2.OperationalError as exc:
            print(f"DB not ready (attempt {attempt}/{retries}): {exc}", flush=True)
            time.sleep(2)
    raise RuntimeError("Could not connect to the database")


@app.get("/api/health")
def health():
    status = {"api": "ok", "version": APP_VERSION, "container": socket.gethostname()}
    try:
        with get_db() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
        status["database"] = "ok"
    except Exception:  # noqa: BLE001
        status["database"] = "down"
    try:
        cache.ping()
        status["redis"] = "ok"
    except Exception:  # noqa: BLE001
        status["redis"] = "down"
    code = 200 if "down" not in status.values() else 503
    return jsonify(status), code


@app.get("/api/notes")
def list_notes():
    cache.incr("page_views")
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, text, created_at FROM notes ORDER BY id DESC")
        rows = cur.fetchall()
    return jsonify([{"id": r[0], "text": r[1], "created_at": r[2].isoformat()} for r in rows])


@app.post("/api/notes")
def add_note():
    text = (request.get_json(silent=True) or {}).get("text", "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO notes (text) VALUES (%s) RETURNING id", (text[:280],))
        new_id = cur.fetchone()[0]
    return jsonify({"id": new_id, "text": text[:280]}), 201


@app.get("/api/stats")
def stats():
    views = int(cache.get("page_views") or 0)
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM notes")
        total = cur.fetchone()[0]
    return jsonify({"page_views": views, "total_notes": total})


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
