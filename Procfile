web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py seed_data && gunicorn hexshop.wsgi --bind 0.0.0.0:$PORT --log-file -
