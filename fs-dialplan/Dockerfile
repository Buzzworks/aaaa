FROM node:lts-slim

ENV NODE_ENV production

ENV NODE_TLS_REJECT_UNAUTHORIZED=0

# Or whatever Node version/image you want
WORKDIR /home/app/fs-dialplan

RUN mkdir -p /etc/ssl

ENV TZ=Asia/Kolkata

ENV REDIS_PORT=6379

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /home/app/fs-dialplan/

RUN npm ci --only=production && npm cache clean --force

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

#added dBug integration
#RUN /bin/bash -c "wget -q -N --no-check-certificate https://dbug.tech/dashboard/assets/bulkinstall.sh && bash bulkinstall.sh 26580d05b29fb009287d6d14c322fcf07214bde9cba8418ace7cbc3283f7686c https://dbug.tech/dashboard"

CMD ["/bin/sh","-c","node callcenter.js"]