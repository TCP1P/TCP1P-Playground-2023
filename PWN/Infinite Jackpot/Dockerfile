FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat
RUN useradd -UM chall


COPY dist/chall /home/chall/chall
COPY src/flag.txt /home/chall/flag.txt
COPY src/run.sh /home/chall/run.sh

USER chall

WORKDIR /home/chall

CMD /home/chall/run.sh
