FROM python:3.7.3

WORKDIR /home

COPY . .

CMD python /home/customhttpserver.py --port 12345
