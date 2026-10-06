# Netxperts DevOps Internship — Docker Project Exercise
## "Ship QuickNotes": containerise a 4-service web app

**Estimated effort:** 8–10 hours across the week
**Due:** before next Sunday's live session (6:30 PM)
**Submit:** a public GitHub repo link + a screenshot of `./check.sh` all green

---

### WHY this exercise?

Almost every DevOps job starts with the same request: *"Here's the app the developers wrote — make it run anywhere."*

This week you are the DevOps engineer. The developers have handed you **QuickNotes**, a small notes app. The code works. It just doesn't run anywhere except their laptops.

Your job: package it, connect it, secure it, shrink it, and publish it.

### WHAT you are building

```
 Browser ──► :8080 ┌──────────┐   public network   ┌──────────┐   private network (internal)
                   │ frontend │ ─────────────────► │   api    │ ──────────┬──────────────┐
                   │  nginx   │   /api/* proxied   │  flask   │           ▼              ▼
                   └──────────┘                    └──────────┘     ┌──────────┐   ┌──────────┐
                                                                    │    db    │   │  redis   │
                                                                    │ postgres │   │  cache   │
                                                                    └────┬─────┘   └────┬─────┘
                                                                     [pgdata]       [redisdata]
```

| Service | Job | Image |
|---|---|---|
| frontend | Serves the web page, forwards `/api/*` to the API | **you build it** |
| api | Python Flask app — stores notes, counts page views | **you build it** |
| db | PostgreSQL — stores notes | `postgres:16-alpine` |
| redis | Page-view counter | `redis:7-alpine` |

### What's in the starter kit

```
quicknotes/
├── api/
│   ├── app.py              ← DON'T change (the developers' code)
│   ├── requirements.txt    ← DON'T change
│   └── Dockerfile          ← TODO (Task 1)
├── frontend/
│   ├── index.html          ← DON'T change
│   ├── nginx.conf          ← TODO (Task 2)
│   └── Dockerfile          ← TODO (Task 2)
├── broken/                 ← Debug challenge (Task 5)
├── docker-compose.yml      ← TODO (Task 3)
├── .env.example            ← copy to .env
├── ANSWERS.md              ← fill in as you go
└── check.sh                ← run this to self-grade
```

**Before you start:** Docker Desktop (or Docker Engine + Compose v2) installed. Check with `docker version` and `docker compose version`.

---

## HOW — the tasks

Work through them in order. Each task builds on the last.

### Task 0 — Set up (15 min)

```bash
git init quicknotes && cd quicknotes      # then copy the starter files in
cp .env.example .env                       # edit: set a real password + your Docker Hub username
git add . && git commit -m "Starter kit"
```

✅ **Done when:** `.env` exists and `git status` does **not** show `.env` (it's in `.gitignore`).

### Task 1 — Dockerise the API (1.5 h)  · 20 marks

Complete every TODO in `api/Dockerfile`.

```bash
docker build -t quicknotes-api:dev ./api
```

The container will crash on its own (no database yet) — **that's expected**. Look at the logs anyway:

```bash
docker run --rm quicknotes-api:dev        # read the error. What is it looking for?
```

✅ **Done when:** the image builds, and `docker run --rm quicknotes-api:dev whoami` does **not** print `root`.

### Task 2 — Dockerise the frontend (45 min)  · 10 marks

Complete `frontend/nginx.conf` and `frontend/Dockerfile`.

✅ **Done when:** `docker build -t quicknotes-frontend:dev ./frontend` succeeds.

### Task 3 — Compose it all together (2 h)  · 25 marks

Complete every TODO in `docker-compose.yml`. Requirements:

1. Only the **frontend** is reachable from your host (port 8080). The API, DB and Redis publish **no** ports.
2. Two networks: `public` (frontend ↔ api) and `private` (api ↔ db ↔ redis). `private` is `internal: true`.
3. All passwords come from `.env` — **zero** secrets written in the compose file or Dockerfiles.
4. Healthchecks on api, db and redis. Startup order uses `condition: service_healthy`.
5. API limited to 0.5 CPU / 256 MB memory, restart policy `unless-stopped`.

```bash
docker compose up -d --build
docker compose ps          # all 4 should be "running", 3 should say "(healthy)"
```

Open **http://localhost:8080** and add a few notes.

✅ **Done when:** the health bar on the page shows `API: ok · DB: ok · Redis: ok`.

### Task 4 — Prove your data survives (30 min)  · 10 marks

```bash
docker compose down        # containers are GONE
docker compose up -d
```

Refresh the page. Your notes must still be there.

Then answer in `ANSWERS.md`: which command would delete the data as well? (Hint: one extra flag.)

✅ **Done when:** notes survive a `down` / `up` cycle, with command output pasted as proof.

### Task 5 — Debug challenge (1.5 h)  · 15 marks

The `broken/` folder holds a Dockerfile and compose file written by "a previous intern". They *sort of* work, but:

- The **Dockerfile** has **5 bad practices** (security, caching, size, process handling).
- The **compose file** has **at least 3 reasons** the API can't reach its dependencies.

For each problem, fill in the table in `ANSWERS.md`: what's wrong, **why** it matters, and your fix. Then fix the files and prove they work.

> Tip: `docker compose -f broken/docker-compose.yml up --build` and read the logs carefully. `docker history <image>` is your friend.

### Task 6 — Make it smaller (1 h)  · 10 marks

1. Record your API image size: `docker images | grep quicknotes-api`
2. Add an `api/.dockerignore`.
3. Convert `api/Dockerfile` to a **multi-stage build** (build wheels in stage 1, copy only them into stage 2).
4. Rebuild and record the new size.

✅ **Done when:** the API image is under **250 MB** and you've filled in the before/after table.

### Task 7 — Publish to Docker Hub (45 min)  · 10 marks

```bash
docker login
docker compose build
docker compose push api frontend
```

Tag with **both** a version (`1.0.0`) and `latest` (hint: `docker tag`). On a fresh machine (or after `docker system prune -a`), prove someone else could run your stack by **pulling** instead of building.

✅ **Done when:** both images appear on your Docker Hub profile. Put the links in `ANSWERS.md`.

---

### Self-check

```bash
./check.sh
```

It tests 20 things: containers, health, the proxy, non-root user, no leaked secrets, network isolation, volumes, image size and limits. **Screenshot the result for your submission.**

---

### GOTCHAS — read these before you ask for help

1. **"Connection refused" to the database** → inside a container, `localhost` means *that container itself*. Use the **service name** (`db`, `redis`, `api`).
2. **`depends_on` alone doesn't wait for Postgres to be ready** — it only waits for it to *start*. That's why you need `condition: service_healthy`.
3. **Changed `.env` but nothing happened?** → `docker compose up -d` again. Changed a Dockerfile? → add `--build`.
4. **`$` in compose healthchecks** → Compose tries to substitute it. Write `$$POSTGRES_USER` to pass a literal `$` to the container.
5. **`docker compose down -v` deletes your volumes** — and all your notes. Don't use `-v` unless you mean it.
6. **Healthcheck always failing?** → slim images have no `curl`. Use a tool that is actually in the image.
7. **Port 8080 already in use?** → something else is on it. Change the *left* side of `8080:80`.
8. **Nginx shows 502 Bad Gateway** → nginx is up but can't reach the API. Check the `proxy_pass` hostname/port, and that both are on the `public` network.

### Bonus (optional, +10)

- **Scan your images:** `docker scout cves <image>` or `trivy image <image>` — fix at least one HIGH finding and explain it.
- **Scale it:** `docker compose up -d --scale api=3`, then `docker compose restart frontend`, refresh the page several times, watch "served by" change. Explain why this works through nginx.
- **CI:** a GitHub Actions workflow that builds and pushes both images on every push to `main`.

### Marking summary

| Task | Marks |
|---|---|
| 1 — API Dockerfile | 20 |
| 2 — Frontend | 10 |
| 3 — Compose | 25 |
| 4 — Persistence | 10 |
| 5 — Debug challenge | 15 |
| 6 — Optimisation | 10 |
| 7 — Registry | 10 |
| **Total** | **100** (+10 bonus) |

Questions? Post them in the internship chat — include the command you ran and the full error message.
