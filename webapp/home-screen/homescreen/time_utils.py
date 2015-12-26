import pytz

class TimeUtils(object):
    def shift_to_timezone(self, date, timezone):
        from_zone = pytz.utc
        to_zone = pytz.timezone(timezone)
        date = date.replace(tzinfo=from_zone)
        updated = date.astimezone(to_zone)
        return updated