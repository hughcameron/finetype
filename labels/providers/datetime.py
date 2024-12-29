"""FineType Provider of data related to date and time."""

from mimesis.providers.date import Datetime as MimesisDatetime


class Datetime(MimesisDatetime):
    """Class for generating data related to the date and time."""


    class Meta:
        name = "datetime"
        datafile = f"{name}.json"
