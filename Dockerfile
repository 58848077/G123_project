FROM python:3.9.10-slim-bullseye

WORKDIR /financial
ADD ./requirements.txt /financial/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /financial/