

def is_valid_postnummer(postnummer):
    """
    Simple offline test wether the input text is a valid norwegian postnummer. A postnummer is a 4 digit number in the
    range of 1000 to 9999. False positives might occur.
    :param postnummer: text be tested for validity
    :return: True if the input might be a valid postnummer and False otherwise.
    """
    try:
        postnummer_n = int(postnummer)
        return postnummer_n > 0 and postnummer_n < 10000 and len(postnummer) == 4
    except:
        return False


def is_valid_wgs_84(latitude, longitude):
    """
    Simple offline test wether a given set of coordinates is valid in the WGS84 coordinate system. False positives might
    occur.
    :param latitude: decimal number with an optional cardinal direction in capital case; 'N', 'S', 'E', 'W'
    :param longitude: decimal number with an optional cardinal direction in capital case; 'N', 'S', 'E', 'W'
    :return: True if the input might be a valid coordinate in WGS84 and False otherwise.
    """
    if not hasattr(latitude, '__getitem__') or not hasattr(longitude, '__getitem__') or len(latitude) == 0 or \
        len(longitude) == 0:
        return False

    value = latitude[-1]
    if value in ['N', 'S', 'E', 'W']:
        latitude = latitude[:-1]

    value = longitude[-1]
    if value in ['N', 'S', 'E', 'W']:
        longitude = longitude[:-1]

    try:
        lat = float(latitude)
        lon = float(longitude)
        return 0.0 <= lat <= 180.0 and 0.0 <= lon <= 180.0
    except:
        return False
