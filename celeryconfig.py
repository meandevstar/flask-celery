# from celery.schedules import crontab


CELERY_IMPORTS = ('src.tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'check-data-blocks': {
        'task': 'src.tasks.check_data_blocks',
        # Every minute
        'schedule': 10,
    }
}