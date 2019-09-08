FROM python:3.7

ENV APP_DIR /app
WORKDIR $APP_DIR

COPY ./ $APP_DIR/
RUN pip install -r requirements.txt

RUN mkdir -p $APP_DIR/var/log
RUN mkdir -p $APP_DIR/static
RUN python manage.py collectstatic --noinput --settings adverity.settings_docker

ENTRYPOINT python manage.py migrate && gunicorn adverity.wsgi:application --workers 3 --timeout 120 --bind :8000