
class CalendarResponse(object):
    """

    """
    def __init__(self):
        self.events = []

    def __json__(self, response):
        return {'events': self.events}


class CalendarEvent(object):
    """

    """
    def __init__(self):
        self.start = ''
        self.end = ''
        self.title = ''
        self.body = ''
        self.link = ''
        self.author = ''

    def __json__(self, response):
        return {'start':self.start, 'end':self.end, 'title':self.title, 'body':self.body, 'link':self.body, 'author':self.author}

