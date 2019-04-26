FROM tiangolo/uwsgi-nginx:python2.7

RUN pip install flask

COPY ./fireline-emu.py /app/main.py
COPY ./responses.json /app/responses.json
