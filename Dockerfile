FROM ubuntu:18.04

RUN apt-get update \
&& apt-get install -y python3.6 \
&& apt-get install -y python3-pip \
&& apt-get install -y locales \
&& apt-get install -y tesseract-ocr \
&& apt-get install -y tesseract-ocr-jpn \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    PYTHONIOENCODING=utf-8

COPY ./requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

COPY . /usr/src/freeai-api
WORKDIR /usr/src/freeai-api

CMD [ "python3", "main.py" ]