FROM php:8.2-apache
COPY ./src /var/www/html
CMD [ "bash", "-c", "SECRET=`cat /proc/sys/kernel/random/uuid` apache2-foreground" ]
