# Share Social Links

Welcome to my (very simplified) clone of Sociobytes - https://sociobytes.com/ by Aashish Chapain. He worked quite hard on it so please check it out.

Tech Stack:

Django
Postgresql
htmx to give some features a SPA feel
NiceAdmin theme by BootstrapMade

While most features are working, this is still a work in progress. While I don't plan on releasing this as a competitor to Sociobytes, I do plan on continuing updating and polishing the applicaiton.

Running the code:

You'll need a .env file in the root that contains the following:

```
SECRET_KEY=
DB_HOST=
DB_NAME=
DB_PASSWORD=
DB_PORT=
DB_USER=
DEBUG=1

ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 
EMAIL_PORT=

EMAIL_USERNAME=
EMAIL_PASSWORD=
FROM_EMAIL=
APP_NAME=

APP_URL=127.0.0.1:8000

DEFAULT_EMAIL=
```

After creating your virtual environment (optional but recommended), install the dependencies.

```
pip install -r requirements.txt
```

Make migrations and apply to the DB.

```
py manage.py makemigrations
py manage.py migrate
```

Finally, run the server.

```
py manage.py runserver
```