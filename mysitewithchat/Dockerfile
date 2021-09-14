FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
RUN mkdir /chat
WORKDIR /chat
ADD . /chat/
RUN pip install -r requirements.txt

