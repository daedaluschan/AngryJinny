FROM python:3

WORKDIR /app

ENV JINNY_KEY=XXXXX \
    JINNY_FILE=/app/jinny.txt

COPY . /app

RUN pip install -r requirements.txt
