from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime


def get_content_type(response):
    CONTENT_TYPES = ['Content-Type', 'content-type']
    content_type = None
    for ct in CONTENT_TYPES:
        if not content_type:
            content_type = response.headers.get(ct)
    return content_type


def http_date(datetime):
    stamp = mktime(datetime.timetuple())
    return format_date_time(stamp)