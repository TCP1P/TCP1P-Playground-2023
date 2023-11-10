FROM --platform=linux/x86_64 python:3.10-slim

ARG DEBIAN_FRONTEND="noninteractive"

RUN apt-get update -y
RUN apt-get install -y socat
RUN mkdir -p /home/ctf/chall

RUN pip3 install --upgrade pip

COPY ./requirements.txt /home/ctf/chall

RUN pip3 install -r /home/ctf/chall/requirements.txt

RUN mkdir -p /home/ctf/chall/src

COPY ./src /home/ctf/chall/src
COPY ./config /home/ctf/chall/src

RUN chown -R root:root /home/ctf/chall

WORKDIR /home/ctf/chall/src

CMD ["./run.sh"]
