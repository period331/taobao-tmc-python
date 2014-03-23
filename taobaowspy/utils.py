# coding: utf-8

from hashlib import md5
import logging
import sys
import time


def gen_sign(app_key, group_name, secret, timestamp=None):

    timestamp = timestamp if timestamp else int(round(time.time() * 1000))
    params = {
        'group_name': group_name,
        'app_key': app_key,
        'timestamp': timestamp,
    }

    param_list = sorted(params.iteritems(), key=lambda d: d[0], reverse=False)

    param_str = secret

    for (key, value) in param_list:
        param_str = param_str + key + str(value)

    param_str += secret

    return md5(param_str).hexdigest().upper()

loggers = {}
log_level = 'DEBUG'


def get_logger(log_name, handlers=None):
    """ 获得日志对象 """

    if log_name in loggers:
        return loggers[log_name]

    logger = logging.getLogger(log_name)

    logger.setLevel(logging.getLevelName(log_level))

    fmt = logging.Formatter('[%(asctime)s] %(levelname)-4s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    handlers = handlers if handlers is not None and isinstance(handlers, list) else []

    handlers.append(logging.StreamHandler(sys.stderr))

    for handler in handlers:
        handler.setFormatter(fmt)
        logger.addHandler(handler)

    loggers[log_name] = logger

    return logger


class Shop(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', '')
        self.session = kwargs.pop('session', '')


