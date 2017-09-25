release: python manage.py migrate
worker: celery -A blutickets worker -l info
web: gunicorn blutickets.wsgi  --worker-class gevent --log-file -