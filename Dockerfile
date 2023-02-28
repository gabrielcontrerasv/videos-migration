FROM python:3.10-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y wget gnupg2 curl unzip libxi6 libgconf-2-4 libcurl4-openssl-dev firefox-esr \
    && GECKODRIVER_VERSION=`curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep tag_name | cut -d '"' -f 4` \
    && wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz \
    && tar -xzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz \
    && rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/geckodriver \
    && chmod +x /usr/local/bin/geckodriver \
    && pip install --upgrade pip \
    && pip install python-dotenv==0.21.1\
    && pip install --no-cache-dir -r requirements.txt 

COPY .env /app/.env
RUN chmod -R 777 /app/clases
CMD ["python", "descargar.py"]

