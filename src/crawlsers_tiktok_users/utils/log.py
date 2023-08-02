"""log"""
import os
from logging.config import dictConfig

from crawler_customsdata.config import settings


def mkdir(path):
    """
    mkdir
    :param path:
    :return:
    """
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)


def init_log():
    """Init log"""
    mkdir(fr'{settings.LOG_PATH}/log')
    default_logging = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            'verbose': {
                'format': '%(asctime)s %(levelname)s %(name)s %(filename)s(%(lineno)d) %(message)s'
            },
            'simple': {
                'format': '%(asctime)s %(levelname)s %(message)s'
            },
        },
        "handlers": {
            "console": {
                "formatter": 'verbose',
                'level': 'DEBUG',
                "class": "logging.StreamHandler",
            },
            'all_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'verbose',
                'filename': os.path.join(settings.LOG_PATH, 'log', 'all.log'),
                'maxBytes': 1024 * 1024 * 1024 * 200,  # 200M
                'backupCount': '5',
                'encoding': 'utf-8'
            },
        },
        "loggers": {
            '': {'level': settings.LOGLEVEL, 'handlers': ['console', 'all_file']},
        }
    }
    dictConfig(default_logging)
