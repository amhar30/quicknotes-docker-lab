#!/usr/bin/env bash
# QuickNotes self-check — run from the project folder AFTER `docker compose up -d --build`
# Usage: ./check.sh
PASS=0; FAIL=0
ok()   { echo "  [PASS] $1"; PASS=$((PASS+1)); }
bad()  { echo "  [FAIL] $1"; FAIL=$((FAIL+1)); }
check(){ if eval "$2" >/dev/null 2>&1; then ok "$1"; else bad "$1"; fi; }

echo "== QuickNotes Docker Lab — self-check =="

echo "-- Containers"
for s in frontend api db redis; do
  check "$s is running" "docker compose ps --status running --services | grep -qx $s"
done
for s in api db redis; do
  check "$s is healthy" "docker inspect -f '{{.State.Health.Status}}' \$(docker compose ps -q $s) | grep -qx healthy"
done

echo "-- App works end-to-end through nginx"
check "frontend page loads on :8080"      "curl -fs http://localhost:8080/ | grep -q QuickNotes"
check "/api/health OK through the proxy"   "curl -fs http://localhost:8080/api/health | grep -q '\"database\":\"ok\"'"
check "can create a note"                  "curl -fs -X POST http://localhost:8080/api/notes -H 'Content-Type: application/json' -d '{\"text\":\"check.sh was here\"}'"

echo "-- Security"
check "api does NOT run as root"           "[ \"\$(docker compose exec -T api whoami)\" != root ]"
check "no password baked into api image"   "! docker image inspect \$(docker compose images -q api) --format '{{json .Config.Env}}' | grep -qi PASSWORD"
check "db port NOT published to the host"  "[ -z \"\$(docker compose port db 5432 2>/dev/null)\" ]"
check "db has no internet access"          "! docker compose exec -T db wget -q -T 3 -O /dev/null http://example.com"
check "base images are pinned (no :latest)" "! grep -Eq '^FROM +[^ :]+( |\$)|^FROM .*:latest' api/Dockerfile frontend/Dockerfile"

echo "-- Persistence"
check "pgdata named volume exists"         "docker volume ls --format '{{.Name}}' | grep -q pgdata"
check "redisdata named volume exists"      "docker volume ls --format '{{.Name}}' | grep -q redisdata"

echo "-- Image hygiene"
SIZE=$(docker image inspect $(docker compose images -q api) --format '{{.Size}}' 2>/dev/null || echo 999999999)
MB=$((SIZE/1024/1024))
if [ "$MB" -lt 250 ]; then ok "api image is ${MB}MB (< 250MB)"; else bad "api image is ${MB}MB (target < 250MB)"; fi
check ".dockerignore exists for api"       "[ -f api/.dockerignore ]"
check "resource limits set on api"         "[ \"\$(docker inspect -f '{{.HostConfig.Memory}}' \$(docker compose ps -q api))\" != 0 ]"

echo
echo "Result: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && echo "All green — take a screenshot of this for your submission!"
exit $FAIL
