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

- Run celery scheduler in every 10 seconds
```bash
	$ celery beat -A app.celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid --max-interval=10
```

- Run celery worker
```bash
	$ celery worker -A app.celery --loglevel=INFO
```
