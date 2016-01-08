# -*- encoding: utf-8 -*-


class WebServiceException(Exception):
    def __init__(self, error=None, status_code=None, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)
        self.status_code = status_code
        self.error = error