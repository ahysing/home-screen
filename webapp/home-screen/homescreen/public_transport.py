class DepartureResponse(object):
    """
    A station or stop with a list of departures from that stop.
    """
    def __init__(self):
        self.departures = []
        self.stop = None

    def __json__(self, request):
        return {'departures': self.departures, 'stop': self.stop}


class Stop(object):
    """
    A bus, rail, ferry or plane stop.
    """
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
    """
    Departure from station.
    """
    def __init__(self):
        self.line_ref = None
        self.direction = None
        self.direction_name = None
        self.destination_display = None
        self.destination_name = None
        self.destination_platform_name = None
        self.aimed_departure_time = None
        self.expected_departure_time = None
        self.delay = None
        self.vehicle_mode = None
        self.published_line_name = None

    def __json__(self, request):
        return {'vehicle_mode': self.vehicle_mode, 'line_ref': self.line_ref,
                'published_line_name': self.published_line_name, 'direction': self.direction,
                'direction_name':self.direction_name,
                'destination_display': self.destination_display, 'destination_name':self.destination_name,
                'delay':self.delay, 'aimed_departure_time':self.aimed_departure_time,
                'expected_departure_time':self.expected_departure_time
                }