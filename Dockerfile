FROM python:3

WORKDIR /app

ENV JINNY_KEY=xxxxx \
    JINNY_DIR=/app/data
ENV JINNY_FILE=${JINNY_DIR}/jinny.txt

COPY . /app

RUN pip3 install -r requirements.txt

# Create storage file directory
RUN mkdir ${JINNY_DIR}
RUN touch ${JINNY_DIR}/jinny.txt
VOLUME ${JINNY_DIR}

CMD bash
