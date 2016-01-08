# -*- encoding: utf-8 -*-
import pytz
import datetime


class TimeUtils(object):
    def shift_to_timezone(self, date, timezone):
        from_zone = pytz.utc
        to_zone = pytz.timezone(timezone)
        date = date.replace(tzinfo=from_zone)
        updated = date.astimezone(to_zone)
        return updated

    def timenow_system_with_timezone(self):
        TIME_ZONE = 'Europe/Oslo'
        dt = datetime.datetime.now()
        return self.shift_to_timezone(dt, TIME_ZONE)

    def timenow_system(self):
        dt = self.timenow_system_with_timezone()
        dt = dt.replace(tzinfo=None)
        return dt