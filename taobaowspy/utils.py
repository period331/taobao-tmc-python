# coding: utf-8

from hashlib import md5

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


