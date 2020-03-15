FROM python:3.7 
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y libsndfile1
WORKDIR /
COPY ./requirements.txt /
RUN pip install -r /requirements.txt
RUN pip install eventlet && pip install gunicorn
COPY . /

