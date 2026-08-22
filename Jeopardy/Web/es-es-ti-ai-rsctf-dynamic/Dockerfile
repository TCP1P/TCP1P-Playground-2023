FROM oven/bun:latest

# Create a non-root user with low privileges
RUN useradd -m -s /bin/bash ctf

WORKDIR /app

# Copy the application source code into the container
COPY ./src .

RUN bun install --production
COPY ./flag.txt /flag.txt
RUN mv /flag.txt /`cat /proc/sys/kernel/random/uuid`.txt

# Change the ownership of the application directory to the non-root user
RUN chown -R ctf:ctf /app

# Create the /app/storage directory if it doesn't exist
RUN mkdir -p /app/storage

# Change the ownership of the /app/storage directory to the non-root user
RUN chown -R ctf:ctf /app/storage

# Switch to the non-root user
USER ctf

# Define the command to run your application
CMD [ "bun", "run", "start" ]

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_7c401a1841d6c31c64f581aa95e85f -e RSCTF_DYNAMIC_FLAG_1a0b7e61d72ec74d13a10a0 {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
USER ctf
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
