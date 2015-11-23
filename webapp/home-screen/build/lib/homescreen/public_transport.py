

class DepartureResponse():
    def __init__(self, departures = []):
        self.departures = departures

    def __json__(self, request):
        return {'departures': self.departures}

class Departure():
    def __init__(self):
        self.line = None 
        self.line_name = None
        self.direction = None
        self.direction_name = None
        self.destination = None
        self.destination_name = None
        self.original_aimed_departure_time = None
        self.destination_aimed_arrival_time = None
        self.delay = None


    def __json__(self, request):
        return {'line': self.line, 'line_name': self.line_name, 'direction': self.direction,
                'direction_name':self.direction_name, 'destination':self.destination,
                'destination_name':self.destination_name, 'delay':self.delay,
                'original_aimed_departure_time':self.original_aimed_departure_time,
                'destination_aimed_arrival_time':self.destination_aimed_arrival_time}