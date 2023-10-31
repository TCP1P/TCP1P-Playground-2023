FROM oven/bun:latest

WORKDIR /app
COPY ./server .
RUN bun run build
ENV FLAG="fake{flag}"
RUN ["bun", "run", "start"]
