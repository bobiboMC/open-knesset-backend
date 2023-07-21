# Pulled Jun 7, 2023
FROM --platform=linux/amd64 python:3.10@sha256:f5ef86211c0ef0db2e3059787088221602cad7e11b238246e406aa7bbd7edc41
RUN pip install --upgrade pip
WORKDIR /srv
COPY gunicorn_conf.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY api ./api
COPY main.py ./
COPY config.py ./
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["gunicorn", "-c", "gunicorn_conf.py", "main:app"]