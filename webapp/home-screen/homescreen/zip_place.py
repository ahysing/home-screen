
class ZipPlace(object):
    def __init__(self, zip = '', latitude = 0.0, longitude = 0.0, place = ''):
        """
        :type longitude: wgs84 longitude for the point
        :type latitude: wgs84 latitude for the point
        :type zip: zip code as issued by the postal service
        """
        self.zip = zip
        self.latitude = latitude
        self.longitude = longitude
        self.place = place

    def __json__(self, request):
        return {'zip': self.zip, 'latitude': self.latitude, 'longitude': self.longitude, 'place': self.place}