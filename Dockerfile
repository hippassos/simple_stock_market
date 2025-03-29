FROM python:3.8

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app

ENV FLASK_CONFIG docker

WORKDIR $APP_HOME

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install --no-cache-dir -r requirements/docker.txt

COPY app app
COPY market.py config.py ./

ENV PORT=5000
# runtime configuration
ENV PATH="venv/bin:$PATH"
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 market:app