FROM node:16.13

RUN apt-get update -y --no-install-recommends
RUN mkdir -p /app
WORKDIR /app
COPY . .

RUN yarn

STOPSIGNAL SIGTERM
CMD ["yarn", "start"]