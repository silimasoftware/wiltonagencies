FROM python:3.11-slim
RUN apt update -y && apt upgrade -y
RUN apt install -y libpq-dev gcc zip
RUN pip install --upgrade pip 
RUN mkdir /usr/src/setup
ADD ./requirements.txt /usr/src/setup
WORKDIR /usr/src/setup
RUN pip install --upgrade -r requirements.txt 
RUN mkdir /usr/src/app
ADD ./website /usr/src/app
WORKDIR /usr/src/app