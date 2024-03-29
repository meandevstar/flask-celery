"""Flask app config and initialization"""
import logging.config

from flask import Flask
from sqlalchemy import orm
from celery import Celery
import celeryconfig


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"]
    )
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


def create_app(config_obj=None):
    """Sets config from passed in config object,
    initializes Flask modules, registers blueprints (routes)

    Args:
        config_obj (class): config class to apply to app

    Returns:
        app: configured and initialized Flask app object

    """
    app = Flask(__name__, static_folder=None)

    if not config_obj:
        logging.warning(
            "No config specified; defaulting to development"
        )
        import config
        config_obj = config.DevelopmentConfig

    app.config.from_object(config_obj)

    from src.models.base import db, migrate
    db.init_app(app)
    db.app = app

    migrate.init_app(app, db)

    from src.routes import register_routes
    register_routes(app)

    return app
