"""FineType Provider of data related to datetimes."""

from babel.dates import format_datetime
from mimesis.providers.date import Datetime as MimesisDatetime


class Datetime(MimesisDatetime):
    """Class for generating data related to the date and time."""

    class Meta:
        name = "datetime"

    def iso_8601(self) -> str:
        """Generate a random date in ISO8601 format.

        :return: Random date in ISO8601 format.
        """
        format = "yyyy-MM-ddTHH:mm:ssXXX"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def iso_8601_ext(self) -> str:
        """Generate a random date in ISO8601 format with microseconds.

        :return: Random date in ISO8601 format with microseconds.
        """
        format = "yyyy-MM-ddTHH:mm:ss.SSSSSSXXX"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def iso_8601_compact(self) -> str:
        """Generate a random date in compact ISO8601 format.

        :return: Random date in compact ISO8601 format.
        """
        format = "yyyyMMddTHHmmss"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def rfc_3339(self) -> str:
        """Generate a random date in RFC3339 format.

        :return: Random date in RFC3339 format.
        """
        format = "yyyy-MM-ddTHH:mm:ss ZZZZ"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def rfc_2822(self) -> str:
        """Generate a random date in RFC2822 format.

        :return: Random date in RFC2822 format.
        """
        format = "EEE, d MMM yyyy HH:mm:ss ZZZZ"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def iso_8601_with_time_zone_name(self) -> str:
        format = "yyyy-MM-ddTHH:mm:ss[XXX|`Z`]"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def rfc_2822_with_ordinals(self) -> str:
        format = "EEE, dd`th` MMM yyyy HH:mm:ss Z"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def unix_timestamp(self) -> str:
        format = "[0-9]+"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def sql_standard(self) -> str:
        format = "yyyy-MM-dd HH:mm:ss"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def american(self) -> str:
        format = "MM/dd/yyyy hh:mm a"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def european(self) -> str:
        format = "dd/MM/yyyy HH:mm"
        return format_datetime(self.datetime(), format=format, locale=self.locale)

    def unix_epoch_in_milliseconds(self) -> str:
        format = "[0-9]+"
        return format_datetime(self.datetime(), format=format, locale=self.locale)
