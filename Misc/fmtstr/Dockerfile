FROM pwn.red/jail
COPY --from=python:3.10 / /srv
WORKDIR /srv/app
COPY /src/run.py ./run
RUN chmod +x run
COPY flag.txt /srv/flag.txt
