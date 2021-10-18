FROM python:3.8-buster
RUN apt-get update && apt-get install sudo nginx binutils libproj-dev gdal-bin libgeos++ proj-bin -y --no-install-recommends

COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
RUN mkdir -p ./app
WORKDIR /app
RUN mkdir -p /pip_cache
COPY . .
RUN pip install -r requirements.txt --cache-dir /pip_cache



RUN chomod -R 777 ./app

RUN chmod +x /app/start-server.sh

STOPSIGNAL SIGTERM
CMD ["/app/start-server.sh"]