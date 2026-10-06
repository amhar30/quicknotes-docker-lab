# This Dockerfile "works on my machine"... but it has 5 problems.
# Find and fix them all. Explain each fix in DEBUG-NOTES.md.
FROM python:latest

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

ENV DB_PASSWORD=SuperSecret123

EXPOSE 5000

CMD python app.py
