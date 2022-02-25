FROM ubuntu:20.04 AS BuildImage

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /home/app/flexydialenv && cd /home/app/

WORKDIR /home/app

COPY requirements.txt /home/app/

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3-pip python3.8-dev libcurl4 curl libpq-dev libcurl4-openssl-dev libssl-dev  swig3.0 unixodbc-dev build-essential libssl-dev libffi-dev wget tzdata\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python && ln -s /usr/bin/swig3.0 /usr/bin/swig \
  && /usr/bin/python3 -m pip install --no-cache --upgrade pip \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/home/app/flexydialenv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 --no-cache install virtualenv && virtualenv flexydialenv \
    && /home/app/flexydialenv/bin/python -m pip install --upgrade pip

RUN pip3 --no-cache install -r ./requirements.txt

FROM ubuntu:20.04 AS Release

USER root

ARG FLEXYDIAL_VERSION="6.0" \
    FLEXYDIAL_BRANCH="main" \
    COMMIT_SHA="0" \
    FLEXYDIAL_IMAGE_REPOSITORY="https://github.com/Buzzworks/flexydial" \
    FLEXYDIAL_IMAGE_DATE_CREATED="2021-11-17"

RUN mkdir -p /home/app && mkdir -p /var/lib/flexydial/media/upload && chmod -R 755 /var/lib/flexydial && cd /home/app/

WORKDIR /home/app

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3 libpython3.8 libcurl4 curl libpq5 libssl1.1  swig3.0 unixodbc libffi7 wget tzdata\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python && ln -s /usr/bin/swig3.0 /usr/bin/swig \
#  && /usr/bin/python3 -m pip install --no-cache --upgrade pip \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/home/app/flexydialenv \
    DEBIAN_FRONTEND=noninteractive LANGUAGE=C.UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8 LC_CTYPE=C.UTF-8 LC_MESSAGES=C.UTF-8 \
    TZ=Asia/Kolkata PYTHONUNBUFFERED="1" DEBUG="False" FREESWITCH_HOST=telephony REDIS_HOST=redis REDIS_PORT=6379 \
    CRM_DB_PORT=5432 FLEXYDIAL_DB_PORT=5432 \
    CRM_DB_USER=postgres FLEXYDIAL_DB_USER=postgres \
    FLEXYDIAL_DB_NAME=flexydial CRM_DB_NAME=crm

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /home/app/

COPY --from=BuildImage /home/app/flexydialenv /home/app/flexydialenv

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

LABEL org.buzzworks.flexydial.distro="ubuntu" \
  org.buzzworks.flexydial.distro.version="focal" \
  org.buzzworks.flexydial.module="flexydial" \
  org.buzzworks.flexydial.component="flexydial-app" \
  org.buzzworks.flexydial.image="flexydial" \
  org.buzzworks.flexydial.version="${FLEXYDIAL_VERSION}" \
  org.buzzworks.flexydial.branch="${FLEXYDIAL_BRANCH}" \
  org.buzzworks.flexydial.revision="${COMMIT_SHA}" \
  org.opencontainers.image.source="${FLEXYDIAL_IMAGE_REPOSITORY}" \
  org.opencontainers.image.created="${FLEXYDIAL_IMAGE_DATE_CREATED}" \
  org.opencontainers.image.authors="ganapathi.chidambaram@flexydial.com" \
  org.opencontainers.image.url="https://flexydial.com" \
  org.opencontainers.image.version="${FLEXYDIAL_VERSION}" \
  org.opencontainers.image.revision="${COMMIT_SHA}" \
  org.opencontainers.image.vendor="Buzzworks Business Services Pvt Ltd" \
  org.opencontainers.image.licenses="Commercial" \
  org.opencontainers.image.ref.name="flexydial" \
  org.opencontainers.image.title="Production flexydial Image" \
  org.opencontainers.image.description="Django Based Dialer App for Freeswitch Telephony"
