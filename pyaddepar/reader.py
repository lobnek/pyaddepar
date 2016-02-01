import pandas as pd
import requests
from csv import reader


class Reader(object):
    def __init__(self, id, key, secret):
        self.__headers = {'Addepar-Firm': id, 'Addepar-Api-Key': key, 'Addepar-Api-Secret': secret}

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

    @property
    def groups(self):
        r = requests.get("https://api.addepar.com/partner/export/csv/groups", headers=self.__headers)
        return self.__toFrame(r)

    @property
    def contacts(self):
        r = requests.get("https://api.addepar.com/partner/export/csv/contacts", headers=self.__headers)
        return self.__toFrame(r)

    def entities(self, start=None, end=None):
        end = end or pd.Timestamp("today")
        start = start or pd.Timestamp("1900-01-01")
        params = {"start_date": self.__format(start), "end_date": self.__format(end)}
        r = requests.get("https://api.addepar.com/partner/export/csv/entities", headers=self.__headers, params=params)
        return self.__toFrame(r)

    def positions(self, date=None):
        date = date or pd.Timestamp("today")
        r = requests.get("https://api.addepar.com/partner/export/csv/positions", headers=self.__headers,
                         params={"date": self.__format(date)})

        return self.__toFrame(r)

    def transactions(self, start, end=None):
        end = end or pd.Timestamp("today")
        params = {"start_date": self.__format(start), "end_date": self.__format(end)}
        r = requests.get("https://api.addepar.com/partner/export/csv/transactions", headers=self.__headers,
                     params=params)
        return self.__toFrame(r)
