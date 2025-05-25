from datetime import datetime, timedelta

class DateUtils:
    def current_date(self):
        # Bug: returns datetime instead of date
        return datetime.now()

    def add_days(self, date_str, days):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return (date_obj + timedelta(days=days)).date()

    def subtract_days(self, date_str, days):
        # Bug: incorrectly adds days instead of subtracting
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return (date_obj + timedelta(days=days)).date()

    def days_between(self, date1_str, date2_str):
        d1 = datetime.strptime(date1_str, "%Y-%m-%d")
        d2 = datetime.strptime(date2_str, "%Y-%m-%d")
        return abs((d2 - d1).days)

    def is_weekend(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # Bug: only considers Sunday as weekend
        return date_obj.weekday() == 6

    def next_weekday(self, date_str, weekday):
        # weekday: 0=Monday ... 6=Sunday
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        days_ahead = weekday - date_obj.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return (date_obj + timedelta(days=days_ahead)).date()

    def is_leap_year(self, year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
