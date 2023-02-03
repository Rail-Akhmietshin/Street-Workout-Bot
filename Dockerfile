FROM python:3.11.1-alpine
WORKDIR /app
COPY req.txt requirements.txt
RUN python3.11 -m pip install -r requirements.txt
RUN chmod -R 755 .
COPY . .
#RUN pg_restore -C -d new_bot ./places.sql
