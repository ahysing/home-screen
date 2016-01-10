# -*- encoding: utf-8 -*-
import pytz
import datetime


class TimeUtils(object):
    def _shift_to_timezone(self, date, timezone):
        from_zone = pytz.utc
        to_zone = pytz.timezone(timezone)
        date = date.replace(tzinfo=from_zone)
        updated = date.astimezone(to_zone)
        return updated

    def systemtime_with_timezone(self):
        time_zone = 'Europe/Oslo'
        dt = datetime.datetime.now()
        return self._shift_to_timezone(dt, time_zone)

    def systemtime(self):
        dt = self.systemtime_with_timezone()
        dt = dt.replace(tzinfo=None)
        return dt