

class WeatherResponse(object):
    """

    """

    def __init__(self):
        self.credit = None
        self.time_forecasts = []

    def __json__(self, request):
        return {'credit': self.credit, 'time_forecasts': self.time_forecasts}


class Credit(object):
    """

    """

    def __init__(self):
        self.url = None
        self.text = None

    def __json__(self, request):
        return {'url': self.url, 'text': self.text}


class Time(object):
    """

    """

    def __init__(self):
        self.start = None
        self.to = None
        self.period = -1
        self.symbol_number = None
        self.symbol_name = None
        self.symbol_number_ex = None
        self.temperature = -1

    def __json__(self, request):
        return {'start': self.start, 'to': self.to, 'period': self.period, 'symbol_number_ex': self.symbol_number_ex,
                'symbol_number': self.symbol_number, 'symbol_name': self.symbol_name, 'temperature': self.temperature}
