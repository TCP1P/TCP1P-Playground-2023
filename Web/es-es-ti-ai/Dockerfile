FROM oven/bun:latest

# Create a non-root user with low privileges
RUN useradd -m -s /bin/bash ctf

WORKDIR /app

# Copy the application source code into the container
COPY ./src .

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
