# Flask API with Celery cron jobs

## Requirements
* Python 3.5+
* SQLite
* Redis

## Starting the server

```bash
	$ cd flask_celery
	$ py -m venv env
	$ pip install -r requirements.txt
	$ $env:FLASK_ENV="development"
	$ flask run
```

## Starting celery cron
Configure Redis for celery, check configcelery.py for more details

```bash
	$ celery beat -A app.celery
```

