class DepartureResponse(object):
    def __init__(self, departures = None):
        if departures:
            self.departures = departures
        else:
            self.departures = []

    def __json__(self, request):
        return {'departures': self.departures}


class Stop(object):
    def __init__(self):
        self.x = None
        self.y = None
        self.id = None
        self.name = None
        self.zone = None
        self.is_hub = False


    def __json__(self, request):
        return {'id':self.id, 'name': self.name, 'zone':self.zone, 'is_hub':self.is_hub, 'y':self.y, 'x':self.x}


class Departure(object):
    def __init__(self):
        self.line_ref = None
        self.line_name = None
        self.direction = None
        self.direction_name = None
        self.destination = None
        self.destination_display = None
        self.destination_name = None
        self.destination_platform_name = None
        self.original_aimed_departure_time = None
        self.destination_aimed_arrival_time = None
        self.delay = None
        self.vehicle_mode = None


    def __json__(self, request):
        return {'vehicle_mode': self.vehicle_mode, 'line_ref': self.line_ref, 'line_name': self.line_name, 'direction': self.direction,
                'direction_name':self.direction_name, 'destination':self.destination, 'destination_display': self.destination_display,
                'destination_name':self.destination_name, 'delay':self.delay,
                'original_aimed_departure_time':self.original_aimed_departure_time,
                'destination_aimed_arrival_time':self.destination_aimed_arrival_time}