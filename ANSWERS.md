# ANSWERS — <Your Name> — Week <N>

## Task 1 — API Dockerfile
1. Why pin the base image instead of using `:latest`?
2. Why copy `requirements.txt` before `app.py`? (Show two `docker build` timings as proof.)
3. Why run as a non-root user? Paste the output of `docker compose exec api whoami`.

## Task 3 — Compose
4. Why can the API reach the database with the hostname `db`?
5. What does `internal: true` do? Paste the output that proves `db` cannot reach the internet.

## Task 4 — Persistence
6. Paste the commands + output proving your notes survived `docker compose down` / `up`.
7. What command would DELETE the data too? (Don't run it until you've answered!)

## Task 5 — Debug challenge
| # | Problem found | Why it is a problem | Your fix |
|---|---------------|---------------------|----------|
| 1 |               |                     |          |
| 2 |               |                     |          |
| 3 |               |                     |          |
| 4 |               |                     |          |
| 5 |               |                     |          |

Compose file problems:

## Task 6 — Optimisation
| Image | Size before | Size after | What you changed |
|-------|-------------|------------|------------------|
| quicknotes-api | | | |

## Task 7 — Registry
Docker Hub links:
- API:
- Frontend:

## Reflection (3–5 sentences)
What was the hardest bug you hit this week, and how did you find it?
