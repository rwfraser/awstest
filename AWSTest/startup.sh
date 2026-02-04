python manage.py collectstatic && gunicorn --workers 2 myproject.wsgi
# use next line AFTER database is set up according to:  https://aws.amazon.com/blogs/containers/deploy-and-scale-django-applications-on-aws-app-runner/ 
# python manage.py migrate && python manage.py collectstatic && gunicorn --workers 2 myproject.wsgi  