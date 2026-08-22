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
COPY ./config/run.sh /home/ctf/chall/src

RUN chown -R root:root /home/ctf/chall
RUN chmod +x /home/ctf/chall/src/run.sh

WORKDIR /home/ctf/chall/src

CMD ["./run.sh"]

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /home/ctf/chall /home/ctf/chall/src /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_f04a414211eaa0dccb5270c9c6562217b8045fc7cacf8b0e -e RSCTF_DYNAMIC_FLAG_e971a4f45ee946727c38c8c16c93abdc2b5c236cd {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
