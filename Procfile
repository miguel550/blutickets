release: python manage.py migrate
web: gunicorn blutickets.wsgi  --worker-class gevent --log-file -