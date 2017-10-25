release: python manage.py migrate; npm run prod; python manage.py collectstatic --no-input
worker: celery -A blutickets worker -l info
web: gunicorn blutickets.wsgi  --worker-class gevent --log-file -