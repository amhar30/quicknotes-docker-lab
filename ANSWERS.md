# ANSWERS — <Your Name> — Week <N>

## Task 1 — API Dockerfile
1. Why pin the base image instead of using `:latest`?

because the application can misperform when the version changes,thats why we use a pinned version.

2. Why copy `requirements.txt` before `app.py`? (Show two `docker build` timings as proof.)

we copy requirements.txt before the app.py because when somthing get changes and when we want to rebuild the image,using cached pip install layer we dont want to reinstall all depencies.thats why we use this order to build the image faster

3. Why run as a non-root user? Paste the output of `docker compose exec api whoami`.

because when we use the root user,if the app has security problems attackers can make dangerous problem ,thats why we create separate user and user group for using the  app and giving it least permission


PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab> docker compose exec api whoami
appuser


## Task 3 — Compose
4. Why can the API reach the database with the hostname `db`?

dokcer compose has dns for the same docker network,so since the api and db is in the same private network. api can use db host name without giving the ip address


5. What does `internal: true` do? Paste the output that proves `db` cannot reach the internet.

PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab\frontend> docker compose exec db wget -T 3 -O /dev/null http://example.com
wget: bad address 'example.com'

What's next:
    Debug this Compose error with Gordon → docker ai "help me fix this compose error" 

## Task 4 — Persistence
6. Paste the commands + output proving your notes survived `docker compose down` / `up`.


PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab\frontend> docker compose down
[+] down 6/6
 ✔ Container quicknotes-frontend-1 Removed                                                                                                                                0.4s
 ✔ Container quicknotes-api-1      Removed                                                                                                                                1.1s
 ✔ Container quicknotes-db-1       Removed                                                                                                                                0.4s
 ✔ Container quicknotes-redis-1    Removed                                                                                                                                0.4s
 ✔ Network quicknotes_public       Removed                                                                                                                                0.2s
 ✔ Network quicknotes_private      Removed                                                                                                                                0.3s
PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab\frontend> docker compose ps                                      
NAME      IMAGE     COMMAND   SERVICE   CREATED   STATUS    PORTS                                                                                                             
PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab\frontend> docker compose down^C                                  
PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab\frontend> docker compose up -d                                   
>> curl http://localhost:8080/api/notes
[+] up 6/6
 ✔ Network quicknotes_private      Created                                                                                                                                0.1s
 ✔ Network quicknotes_public       Created                                                                                                                                0.1s
 ✔ Container quicknotes-db-1       Healthy                                                                                                                                6.5s
 ✔ Container quicknotes-redis-1    Healthy                                                                                                                                6.1s
 ✔ Container quicknotes-api-1      Healthy                                                                                                                               12.1s
 ✔ Container quicknotes-frontend-1 Started                                                                                                                               12.3s


StatusCode        : 200
StatusDescription : OK
Content           : [{"created_at":"2026-10-08T14:20:47.521516","id":3,"text":"docker is awesome"},{"created_at":"2026-10-08T14:20:38.068053","id":2,"text":"docker is 
                    easy"},{"created_at":"2026-10-08T14:20:29.515307","id...
RawContent        : HTTP/1.1 200 OK
                    Connection: keep-alive
                    Content-Length: 229
                    Content-Type: application/json
                    Date: Thu, 08 Oct 2026 15:28:21 GMT
                    Server: nginx/1.27.5
                    
                    [{"created_at":"2026-10-08T14:20:47.521516","...
Forms             : {}
Headers           : {[Connection, keep-alive], [Content-Length, 229], [Content-Type, application/json], [Date, Thu, 08 Oct 2026 15:28:21 GMT]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 229



PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab\frontend>


7. What command would DELETE the data too? (Don't run it until you've answered!)

docker compose down -v

## Task 5 — Debug challenge

1. unpinned image

problem?

    python:latest

why its a problem?

    every time pulling a latest python version makes the app to misperform because the change of the versions

fix?

    using a pinned image ,example- python:3.12-slim ,so the application specifically build on it and gives the maximum its performance as it is


2. copying files even before installing depandacies

problem?

    copying files even before installing depandacies

why its a problem?

    this will make the build to start from scratch ,will take long time and that order doesnt allow to use the cache

fix?

    installing the dependacies and then copying the app.py is best practice.so when code is changes it doesnt need to reinstall pip,gets it from cache and only rebuild the app.py

3. root user

problem?

    container uses root user to run the app

why its a problem?

    if the app has security vulnerability and a attacker expoloits it,then there is huge risk because of the root uses permissions

fix?

    creating separate user with least access priviledge


4. env
problem?

    password is hardcoded

why its a problem?

    password should not be baked into the docker image

fix?

remove it from there and providing it in the run time env configuration 


5. CMD python app.py

problem?

    uses shell form and starts the flask app the directly

why its a problem?

    it doesnt provide the required production server and doesnt provide exec process handling

fix?

    starting the app with gunicorn using exec/json






Compose file problems:

1. 

problem?

    DB_HOST: localhost

why its a problem?

    Inside the API container, localhost means the API container, not the PostgreSQL container.

fix?

    Use DB_HOST: db.

2. 

problem?

    The redis service is missing.

why its a problem?

    There is no Redis container/service for the API to connect to.

fix?

    Add the required redis service using redis:7-alpine.

3. 

problem?

    POSTGRES_DB and POSTGRES_USER are missing, and the password is hard-coded

why its a problem?

    The database configuration does not match the application's expected database name/user configuration, and the password is exposed in the Compose file.

fix?

    Using POSTGRES_DB: ${DB_NAME}, POSTGRES_USER: ${DB_USER}, and POSTGRES_PASSWORD: ${DB_PASSWORD} from .env.

4. 

problem?

    The API is exposed with 5000:5000.

why its a problem?

    The API should not be directly reachable from the host; only the frontend should be exposed.

fix?

    Remove the API ports: mapping and allow the frontend to reach it through the Docker network.

5. 

problem?

    no healthchecks based dependancies in the configurations

why its a problem?

    api starts even before the db, redis are ready 

fix?

    Adding depends_on with condition: service_healthy for both db and redis.

## Task 6 — Optimisation
| Image          | Size before           | Size after | What you changed |
|-------         |                       |------------|------------------|
| quicknotes-api |before-215 mb          | after 223mb|

what i have changed;-

chaged that to multistage  build .builder stage create python wheels and runtime stage installs the wheels exclude the builder stage tools|

## Task 7 — Registry
Docker Hub links:
- API:   https://hub.docker.com/r/amhar30/quicknotes-api
- Frontend:   https://hub.docker.com/r/amhar30/quicknotes-frontend


output;


PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab> docker image rm amhar30/quicknotes-api:1.0.0 amhar30/quicknotes-frontend:1.0.0
Untagged: amhar30/quicknotes-api:1.0.0
Untagged: amhar30/quicknotes-frontend:1.0.0
PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab> docker compose pull
[+] pull 4/4
 ✔ Image postgres:16-alpine                Pulled                                                                                                2.7s
 ✔ Image amhar30/quicknotes-frontend:1.0.0 Pulled                                                                                                3.3s
 ✔ Image redis:7-alpine                    Pulled                                                                                                3.3s
 ✔ Image amhar30/quicknotes-api:1.0.0      Pulled                                                                                                3.3s
PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab> docker compose up -d --no-build
[+] up 6/6
 ✔ Network quicknotes_private      Created                                                                                                       0.2s
 ✔ Network quicknotes_public       Created                                                                                                       0.1s
 ✔ Container quicknotes-redis-1    Healthy                                                                                                       6.4s
 ✔ Container quicknotes-db-1       Healthy                                                                                                       6.9s
 ✔ Container quicknotes-api-1      Healthy                                                                                                      13.1s
 ✔ Container quicknotes-frontend-1 Started                                                                                                      13.4s
PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab> docker compose ps
NAME                    IMAGE                               COMMAND                  SERVICE    CREATED          STATUS                    PORTS
quicknotes-api-1        amhar30/quicknotes-api:1.0.0        "gunicorn --bind 0.0…"   api        22 seconds ago   Up 16 seconds (healthy)   5000/tcp
quicknotes-db-1         postgres:16-alpine                  "docker-entrypoint.s…"   db         22 seconds ago   Up 21 seconds (healthy)   5432/tcp
quicknotes-frontend-1   amhar30/quicknotes-frontend:1.0.0   "/docker-entrypoint.…"   frontend   22 seconds ago   Up 9 seconds (healthy)    0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
quicknotes-redis-1      redis:7-alpine                      "docker-entrypoint.s…"   redis      22 seconds ago   Up 22 seconds (healthy)   6379/tcp
PS C:\Users\asus\Desktop\Internship\Assignment-4 pending\quicknotes-docker-lab-STUDENT\quicknotes-docker-lab> 




## Reflection (3–5 sentences)
What was the hardest bug you hit this week, and how did you find it?

hardest bugs were in the week was to nginx healthcheck failure and db-port check report failure even though the db port is not exposed to the host.
i investigated the nginx problem by testing localhost and 127.0.0.1 in the frontend container. the issue is from the ipv6 while the nginx is listening on ipv4. adding listen [::]:80; solved that, for db port check,docker inspect showed,theres no port binded to host port,but docker port db 5432 gave invalid ip:0 i updated the self check to inspect actual host port bindings then 20 checks passed.also i corrected the dokcer hub user name when the push failed 