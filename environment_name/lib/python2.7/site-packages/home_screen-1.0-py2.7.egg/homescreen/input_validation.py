

def is_valid_postnummer(postnummer):
    try:
        postnummer_n = int(postnummer)
        return postnummer_n > 0 and postnummer_n < 10000 and len(postnummer) == 4
    except:
        return False

def is_valid_wgs_84(latitude, longitude):
    if not hasattr(latitude, '__getitem__') or not hasattr(longitude, '__getitem__') or len(latitude) == 0 or len(longitude) == 0:
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
