FROM python:3
LABEL maintainer="iharrando@linagora.com"

WORKDIR /usr/src/app

# System dependencies
RUN apt-get update

# Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY nlp /usr/src/app/nlp
COPY docker-entrypoint.sh wait-for-it.sh ./
COPY supervisor /usr/src/app/supervisor
RUN mkdir -p /var/log/supervisor/
RUN mkdir /usr/src/app/logs
RUN chmod +x docker-entrypoint.sh wait-for-it.sh

ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app/nlp"

HEALTHCHECK CMD curl localhost:80/healthcheck

EXPOSE 80

ENTRYPOINT ["./docker-entrypoint.sh"]

