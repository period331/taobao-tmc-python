# coding: utf-8

from hashlib import md5

import time

def createSign(app_key, group_name, secret, timestamp=None):

    timestamp = timestamp if timestamp else int(round(time.time() * 1000))
    signParams = {
        'group_name': group_name,
        'app_key': app_key,
        'timestamp': timestamp,
    }

    param_list = sorted(signParams.iteritems(), key=lambda d: d[0], reverse=False)

    param_str = secret

    for (key, value) in param_list:
        param_str = param_str + key + str(value)

    param_str += secret

    print param_str

    return md5(param_str).hexdigest().upper()


