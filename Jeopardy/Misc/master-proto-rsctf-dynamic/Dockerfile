# check=skip=JSONArgsRecommended
FROM oven/bun:latest as builder

RUN apt-get update && apt-get install -yq socat procps

WORKDIR /app
COPY flag.txt /flag.txt
COPY ./src/index.js ./index.js
USER 404
CMD socat -T30 tcp-listen:1337,fork,reuseaddr exec:"bun index.js",pty,raw,stderr

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /app/index.js /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_90f4d8f9a78acf6a559e97560ef0a496 -e RSCTF_DYNAMIC_FLAG_5631b13c8e8b1a3e985b704a5 {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
USER 404
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
