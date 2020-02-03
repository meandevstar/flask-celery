import logging
import os

logger = logging.getLogger(__name__)


class DevelopmentConfig(object):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/db.sqlite"

    HOST = "localhost"
    PORT = "5000"
    SECRET_KEY = "test"
    ENCRYPTION_KEY = "test"

    REDIS_HOST = "0.0.0.0"
    REDIS_PORT = 6379
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', "redis://{host}:{port}/0".format(
        host=REDIS_HOST, port=str(REDIS_PORT)))
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
