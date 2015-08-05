# coding: utf-8
__author__ = 'baocaixiong'

from message import ConfirmMessage, QueryMessage
from messageio import writer


def confirm_message(message_id, token):
    cm = ConfirmMessage()
    cm.token = token
    cm.update_content({'id': message_id})

    return writer(cm)


query_message = lambda **kwargs: writer(QueryMessage(**kwargs))
