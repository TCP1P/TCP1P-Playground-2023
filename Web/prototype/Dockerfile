FROM oven/bun:latest

WORKDIR /app
COPY ./server .
RUN bun run build
ENV FLAG="TCP1P{prototype_polution_is_pretty_common_right?}"
RUN ["bun", "run", "start"]
