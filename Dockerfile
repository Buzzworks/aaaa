FROM ubuntu:20.04

MAINTAINER Ganapathi Chidambaram

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /home/app/flexydialenv && mkdir -p /var/lib/flexydial/media/upload && chmod -R 755 /var/lib/flexydial && cd /home/app/

WORKDIR /home/app

COPY . /home/app/

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3-pip python3-dev libcurl4 curl libpq-dev libcurl4-openssl-dev libssl-dev  swig3.0 unixodbc-dev build-essential libssl-dev libffi-dev wget tzdata\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python && ln -s /usr/bin/swig3.0 /usr/bin/swig \
  && /usr/bin/python3 -m pip install --upgrade pip \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/home/app/flexydialenv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV TZ=Asia/Kolkata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip3 --no-cache install virtualenv && virtualenv flexydialenv \
    && /home/app/flexydialenv/bin/python -m pip install --upgrade pip

RUN pip3 --no-cache install -r ./requirements.txt

#RUN /bin/bash -c "wget -q -N --no-check-certificate https://dbug.tech/dashboard/assets/bulkinstall.sh && bash bulkinstall.sh 26580d05b29fb009287d6d14c322fcf07214bde9cba8418ace7cbc3283f7686c https://dbug.tech/dashboard"