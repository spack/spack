FROM python:3.7-alpine

RUN pip install pygithub

ADD entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
