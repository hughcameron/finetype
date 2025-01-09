"""FineType Provider of data related to datetimes."""

from babel.dates import format_datetime
from mimesis.providers.date import Datetime as MimesisDatetime


class Date(MimesisDatetime):
    """Class for generating data related to the date and time."""

    class Meta:
        name = "date"
        # datafile = f"{name}.json"

    def short_ymd(self) -> str:
        format = "yy-MM-dd"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def short_dmy(self) -> str:
        format = "dd-MM-yy"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def short_mdy(self) -> str:
        format = "MM-dd-yy"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def numeric_ymd(self) -> str:
        format = "yyyyMMdd"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def numeric_dmy(self) -> str:
        format = "ddMMyyyy"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def numeric_mdy(self) -> str:
        format = "MMddyyyy"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def long_full_month_name(self) -> str:
        format = "MMMM d, y"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def long_weekday_month_name(self) -> str:
        format = "EEEE, d MMMM y"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def abbreviated_month(self) -> str:
        format = "MMM d, y"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def full_weekday_abbreviated_month(self) -> str:
        format = "EEEE, d MMM y"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def julian(self) -> str:
        format = "yy-DDD"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def ordinal(self) -> str:
        format = "yyyy-DDD"
        return format_datetime(self.datetime(), format=format, locale=self.locale)
