import pandas as pd
import requests
import logging
from csv import reader


class Reader(object):
    def __init__(self, id, key, secret, logger=None):
        self.__headers = {'Addepar-Firm': id, 'Addepar-Api-Key': key, 'Addepar-Api-Secret': secret}
        self.__address = "https://api.addepar.com/partner/export/csv/"
        self.__logger = logger or logging.getLogger(__name__)

    @staticmethod
    def __toFrame(r):
        # construct the decoded rows
        rows = [a.decode() for a in r.iter_lines()]
        # parse them into lists of strings, note that a comma between " " double-quotes is ignored
        # compare with http://tinyurl.com/gn7kmvu
        lines = [line for line in reader(rows)]

        return pd.DataFrame(columns=lines[0], data=lines[1:])

    @staticmethod
    def __format(t):
        return t.strftime("%Y-%m-%d")

    #todo: Needs refactoring, one element can be in multiple groups
    @property
    def groups(self):
        r = requests.get(self.__address + "groups", headers=self.__headers)
        b = self.entities()["Name"]
        b = pd.Series(index=b.values, data=b.index)
        a = self.__toFrame(r).set_index(keys=["Member Name"])
        return pd.concat((a, b), join="inner", axis=1)


    @property
    def contacts(self):
        r = requests.get(self.__address + "contacts", headers=self.__headers)
        return self.__toFrame(r)

    def entities(self, start=None, end=None):
        end = end or pd.Timestamp("today")
        start = start or pd.Timestamp("1900-01-01")
        params = {"start_date": self.__format(start), "end_date": self.__format(end)}
        r = requests.get(self.__address + "entities", headers=self.__headers, params=params)
        return self.__toFrame(r).set_index("ID")

    def positions(self, date=None):
        date = date or pd.Timestamp("today")
        params = {"date": self.__format(date)}
        r = requests.get(self.__address + "positions", headers=self.__headers, params=params)
        return self.__toFrame(r).set_index(keys=["Owner ID", "Owned ID"])

    def transactions(self, start=None, end=None):
        end = end or pd.Timestamp("today")
        start = start or pd.Timestamp("1900-01-01")
        params = {"start_date": self.__format(start), "end_date": self.__format(end)}
        r = requests.get(self.__address + "transactions", headers=self.__headers, params=params)
        return self.__toFrame(r).set_index(keys=["Transaction ID","Type","Posted Date","Date","Owner ID", "Owned ID"])

    @property
    def owner(self):
        ids = self.positions().index.get_level_values(level=0).unique()
        return(self.entities().ix[ids])

    @property
    def products(self):
        ids = self.positions().index.get_level_values(level=1).unique()
        return(self.entities().ix[ids])
