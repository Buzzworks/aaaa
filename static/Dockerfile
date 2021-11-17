FROM busybox
ARG FLEXYDIAL_VERSION="6.0"
ARG FLEXYDIAL_BRANCH="main"
ARG COMMIT_SHA="0"
ARG FLEXYDIAL_IMAGE_REPOSITORY="https://github.com/Buzzworks/flexydial"
ARG FLEXYDIAL_IMAGE_DATE_CREATED="2021-11-17"
RUN mkdir -p /home/app/static
WORKDIR /home/app
LABEL org.buzzworks.flexydial.distro="ubuntu" \
  org.buzzworks.flexydial.distro.version="focal" \
  org.buzzworks.flexydial.module="flexydial" \
  org.buzzworks.flexydial.component="flexydial-static" \
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
  org.opencontainers.image.ref.name="flexydial-static" \
  org.opencontainers.image.title="Production flexydial Static File Image" \
  org.opencontainers.image.description="Static Files required for Flexydial"
COPY . /home/app/static
