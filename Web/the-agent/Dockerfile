FROM php:latest

RUN useradd -m -s /bin/bash ctf

RUN mkdir /challenge

COPY ./src /challenge

RUN chmod 755 -R /challenge

USER ctf

CMD php -S 0.0.0.0:80 -t /challenge
