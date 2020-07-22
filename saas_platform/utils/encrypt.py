import hashlib

from django.conf import settings


def md5(string):
    has_obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    has_obj.update(string.encode('utf-8'))
    return has_obj.hexdigest()