FROM node:lts-slim

ENV NODE_ENV production \
    NODE_TLS_REJECT_UNAUTHORIZED=0 \
    TINI_VERSION v0.19.0 \
    TZ=Asia/Kolkata \
    REDIS_PORT=6379

ARG FLEXYDIAL_VERSION="6.0"
ARG FLEXYDIAL_BRANCH="main"
ARG COMMIT_SHA="0"
ARG FLEXYDIAL_IMAGE_REPOSITORY="https://github.com/Buzzworks/flexydial"
ARG FLEXYDIAL_IMAGE_DATE_CREATED="2021-11-17"

# Or whatever Node version/image you want
WORKDIR /home/app/fs-dialplan

RUN mkdir -p /etc/ssl

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /home/app/fs-dialplan/

RUN npm ci --only=production && npm cache clean --force

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

LABEL org.buzzworks.flexydial.distro="ubuntu" \
  org.buzzworks.flexydial.distro.version="focal" \
  org.buzzworks.flexydial.module="flexydial" \
  org.buzzworks.flexydial.component="flexydial-websocket" \
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
  org.opencontainers.image.ref.name="flexydial-websocket" \
  org.opencontainers.image.title="Production flexydial Websocket Image" \
  org.opencontainers.image.description="NodeJS App for Websocket Connection for Flexydial"

CMD ["/bin/sh","-c","node callcenter.js"]