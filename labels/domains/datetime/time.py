"""FineType Provider of data related to datetimes."""

from mimesis.providers.date import Datetime as MimesisDatetime


class Time(MimesisDatetime):
    """Class for generating data related to the date and time."""

    class Meta:
        name = "time"
