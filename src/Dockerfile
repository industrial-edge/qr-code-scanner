FROM python:3.8-alpine

WORKDIR /usr/src/app

RUN apk add build-base  && \
    apk add libffi-dev  && \
    apk add python3-dev && \
    pip install evdev   && \
    pip install paho-mqtt && \
    apk del python3-dev && \
    apk del libffi-dev && \
    apk del build-base

COPY main.py .

CMD [ "python", "./main.py" ]