FROM python:3.7-slim

RUN mkdir /app
WORKDIR /app

COPY ./src /app
RUN pip install psycopg2-binary
CMD ["python3", "server.py"]
