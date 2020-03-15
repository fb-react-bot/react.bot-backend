FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-devel
RUN pip install -U flask
WORKDIR /
COPY ./requirements.txt /
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y libsndfile1
RUN pip install -r /requirements.txt
RUN pip install librosa
COPY . /