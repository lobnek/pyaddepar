import pandas as pd
import requests
import logging
from csv import reader


class AddeparError(Exception):
    """
    Problem with the reader
    """


class Reader(object):
    def __init__(self, id, key, secret, logger=None):
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

            r.raise_for_status()
            return r

        except Exception as e:
            raise AddeparError(e)


    @staticmethod
    def __toFrame(r):
        try:
            # construct the decoded rows
            rows = [a.decode() for a in r.iter_lines()]
            # parse them into lists of strings, note that a comma between " " double-quotes is ignored
            # compare with http://tinyurl.com/gn7kmvu
            lines = [line for line in reader(rows)]
            return pd.DataFrame(columns=lines[0], data=lines[1:])

        except Exception as e:
            raise AddeparError(e)

    @staticmethod
    def __format(t):
        return t.strftime("%Y-%m-%d")

    @property
    def groups(self):
        r = self.__request("groups")

        # todo: this is an unfortunate construction. It would be nice if the requests for groups returns rows with
        # todo: group name, member name and ID of the member in the entities table
        b = self.entities()["Name"]
        b = pd.Series(index=b.values, data=b.index)
        a = self.__toFrame(r)
        a["ID"] = a["Member Name"].apply(lambda x: b[x])
        return a.set_index(keys=["Group Name", "Member Name"])

    @property
    def contacts(self):
        """
        A DataFrame of all contacts stored
        """
        r = self.__request("contacts")
        return self.__toFrame(r).set_index("ID")

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
        r = self.__request("entities", params=params)

        return self.__toFrame(r).set_index("ID")

    def positions(self, date=None):
        """
        Return a DataFrame of positions held on a particular day

        :param date: The date, use today if not specified
        :return: DataFrame with MultiIndex ["Owner ID", "Owned ID"]
        """
        date = date or pd.Timestamp("today")
        r = self.__request("positions", params={"date": self.__format(date)})
        return self.__toFrame(r).set_index(keys=["Owner ID", "Owned ID"])

    def transactions(self, start=None, end=None):
        end = end or pd.Timestamp("today")
        start = start or pd.Timestamp("1900-01-01")
        params = {"start_date": self.__format(start), "end_date": self.__format(end)}
        r = self.__request("transactions", params=params)

        return self.__toFrame(r).set_index(
            keys=["Transaction ID", "Type", "Posted Date", "Date", "Owner ID", "Owned ID"])

    def owner(self, date=None):
        """
        Return all owners (e.g. a subset of entities) on a specific date

        :param date: The date for the underlying positions snapshot, use today if not specified
        :return: entities
        """
        date = date or pd.Timestamp("today")
        ids = self.positions(date).index.get_level_values(level="Owner ID").unique()
        return self.entities().ix[ids]

    def products(self, date=None):
        """
        Return all produts owned (e.g. a subset of entities) on a specific date

        :param date: The date for the underlying positions snapshot, use today if not specified
        :return: entities
        """
        date = date or pd.Timestamp("today")
        ids = self.positions(date).index.get_level_values(level="Owned ID").unique()
        return self.entities().ix[ids]
