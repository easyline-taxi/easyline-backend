FROM python:3.7-buster

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
RUN mkdir -p ./app
WORKDIR /app
RUN mkdir -p /pip_cache
COPY . .
RUN pip install -r requirements.txt --cache-dir /pip_cache

RUN chown -R www-data:www-data ./

STOPSIGNAL SIGTERM
CMD ["/app/start-server.sh"]