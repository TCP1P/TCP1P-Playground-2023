FROM ubuntu:latest
WORKDIR /app

COPY ./src/src.tar.gz .

RUN tar -C /app -xzvf /app/src.tar.gz
RUN rm -f /app/src.tar.gz

CMD ["./src"]