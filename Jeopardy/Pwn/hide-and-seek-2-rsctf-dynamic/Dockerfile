# check=skip=JSONArgsRecommended
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat
RUN useradd -UM chall

COPY dist/chall /home/chall/chall
COPY src/flag.txt /flag.txt
COPY src/run.sh /home/chall/run.sh

USER chall

WORKDIR /home/chall

CMD /home/chall/run.sh

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /home/chall/run.sh /home/chall/chall /home/chall /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_fac3775e3f5818642e4b0fc -e RSCTF_DYNAMIC_FLAG_94d7d6d7d73b9d2b {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
USER chall
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
