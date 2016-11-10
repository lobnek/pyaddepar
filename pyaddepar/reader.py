import pandas as pd
import requests
import logging

from pyaddepar.parser import request2frame, parse
import os


class AddeparError(Exception):
    """
    Problem with the reader
    """


class Reader(object):
    def __init__(self, id=None, key=None, secret=None, logger=None):
        id = id or os.environ["AFIRM"]
        key = key or os.environ["AKEY"]
        secret = secret or os.environ["ASECRET"]
        self.__headers = {'Addepar-Firm': id, 'Addepar-Api-Key': key, 'Addepar-Api-Secret': secret}
        self.__address = "https://api.addepar.com/partner/export/csv/"
        self.__logger = logger or logging.getLogger(__name__)

    def __repr__(self):
        return "Addepar REST api running on {} with headers {}".format(self.__address, self.__headers)

    def __request(self, name, params=None):
        try:
            self.__logger.debug("Address {0}".format(self.__address + name))
            self.__logger.debug("Params {0}".format(params))

            r = requests.get(self.__address + name, headers=self.__headers, params=params)
            self.__logger.debug("Status code {0}".format(r.status_code))

            # only raises if there for status code 400 <= to < 600
            # todo: Are there any error codes with 300? Shall we raise if error code is not 200?
            r.raise_for_status()
            return request2frame(r.iter_lines())

        except Exception as e:
            raise AddeparError(e)

    @staticmethod
    def __format(t):
        return t.strftime("%Y-%m-%d")

    @property
    def groups(self):
        return parse(self.__request("groups"), index=["Group ID", "Member ID"])

    @property
    def contacts(self):
        """
        A DataFrame of all contacts stored
        """
        return parse(self.__request("contacts"), dates=["Birthday"], index=["ID"])

    def entities(self, start=None, end=None):
        """
        All entities contained in the database, these are the nodes of a huge graph
        :param start: The start date, use "1900-01-01" if not specified
        :param end: The end date, use today if not specified

        :return: DataFrame
        """
        end = end or pd.Timestamp("today")
        start = start or pd.Timestamp("1900-01-01")
        params = {"start_date": self.__format(start), "end_date": self.__format(end)}
        frame = self.__request("entities", params=params)

        dates = [key for key in frame.keys() if key.endswith("Date")]
        return parse(frame, dates=dates, index="ID")

    def positions(self, date=None):
        """
        Return a DataFrame of positions held on a particular day

        :param date: The date, use today if not specified
        :return: DataFrame with MultiIndex ["Owner ID", "Owned ID"]
        """
        date = date or pd.Timestamp("today")
        frame = self.__request(name="positions", params={"date": self.__format(date)})
        return parse(frame=frame, dates=["Date"],
                     numbers=["Units", "Value", "Adjusted Value", "Original Cost Basis", "Adjusted Cost Basis",
                              "Calculated Accrued", "Accrued", "Principal Factor"],
                     index=["Owner ID", "Owned ID"]).sortlevel(level=0)

    def transactions(self, start=None, end=None):
        end = end or pd.Timestamp("today")
        start = start or pd.Timestamp("1900-01-01")
        params = {"start_date": self.__format(start), "end_date": self.__format(end)}
        p = parse(self.__request("transactions", params=params), dates=["Posted Date", "Date"])
        # index=["Owner ID", "Owned ID", "Date", "Transaction ID"])

        # todo: THIS HAS TO GO!!!!!! The construction is weird
        columns = [a for a in p.keys() if a.startswith("Tag")]
        p["Tag"] = p[columns].sum(axis=1)

        rows = p["Owner ID"] == ""
        p["Owner ID"][rows] = p["Owned ID"][rows]
        p = p.set_index(keys=["Owner ID", "Owned ID", "Date", "Transaction ID"])
        return p.drop(labels=columns, axis=1)

