# -*- encoding: utf-8 -*-
from wsgiref.handlers import format_date_time
from time import mktime


def get_content_type(response):
    content_types = ['Content-Type', 'content-type']
    content_type = None
    for ct in content_types:
        if not content_type:
            content_type = response.headers.get(ct)
    return content_type


def http_date(dt):
    stamp = mktime(dt.timetuple())
    return format_date_time(stamp)