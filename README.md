# Element Watcher
Django web app for watching html elements on a web page. Add an element
you want to watch using a css selector, the interval time, and a callback
url that will be called when the elements value has changed. Authenticate
with django default accounts of twitter using django-all-auth. Demo site:
https://murmuring-wave-93908.herokuapp.com/

# Setup
- clone repo
- create virtualenv and activate
- <code>pip install -r requirements.txt</code>
- cd into <project_name>/element_watch
- <code>docker-compose up</code> - for service dependencies
- <code>python manage.py migrate</code>
- <code>python manage.py runserver</code>

# Tests
- <code>python manage.py test</cod>

# Dependencies
- python 3.6
- rabbitmq
- postgres
- celery 4
