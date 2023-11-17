FROM oven/bun:latest as builder

RUN apt-get update && apt-get install -yq socat procps

WORKDIR /app
COPY flag.txt /flag.txt
COPY ./src/index.js ./index.js
USER 404
CMD socat -T30 tcp-listen:1337,fork,reuseaddr exec:"bun index.js",pty,raw,stderr
