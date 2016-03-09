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
    def __parse(request):
        try:
            rows = [a.decode() for a in request]
            assert len(rows) >= 1
            # parse them into lists of strings, note that a comma between " " double-quotes is ignored
            # compare with http://tinyurl.com/gn7kmvu
            lines = [line for line in reader(rows)]
            return pd.DataFrame(columns=lines[0], data=lines[1:])
        except Exception as e:
            raise AddeparError(e)

    @staticmethod
    def __date_safe(x):
        return pd.to_datetime(x, errors="coerce", exact=True, format="%m/%d/%Y").date()

    @staticmethod
    def __apply(frame, dates, index=None):
        for key in dates:
            frame[key] = frame[key].apply(Reader.__date_safe)

        not_dates = [k for k in frame.keys() if k not in dates]
        frame[not_dates] = frame[not_dates].apply(pd.to_numeric, errors="ignore")

        if index:
            return frame.set_index(index)
        else:
            return frame

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
        a = self.__parse(r.iter_lines())

        a["ID"] = a["Member Name"].apply(lambda x: b[x])
        return self.__apply(a, [], index=["Group Name", "Member Name"])

    @property
    def contacts(self):
        """
        A DataFrame of all contacts stored
        """
        f = self.__parse(self.__request("contacts").iter_lines())
        return self.__apply(f, dates=["Birthday"], index="ID")

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
        frame = self.__parse(self.__request("entities", params=params).iter_lines())

        dates = [key for key in frame.keys() if key.endswith("Date")]
        return self.__apply(frame, dates=dates, index="ID")

    def positions(self, date=None):
        """
        Return a DataFrame of positions held on a particular day

        :param date: The date, use today if not specified
        :return: DataFrame with MultiIndex ["Owner ID", "Owned ID"]
        """
        date = date or pd.Timestamp("today")
        frame = self.__parse(self.__request(name="positions", params={"date": self.__format(date)}).iter_lines())
        return self.__apply(frame=frame, dates=["Date"], index=["Owner ID", "Owned ID"])

    def transactions(self, start=None, end=None):
        end = end or pd.Timestamp("today")
        start = start or pd.Timestamp("1900-01-01")
        params = {"start_date": self.__format(start), "end_date": self.__format(end)}
        frame = self.__parse(self.__request("transactions", params=params).iter_lines())
        return self.__apply(frame, dates=["Posted Date", "Date"],
                            index=["Transaction ID", "Type", "Posted Date", "Date", "Owner ID", "Owned ID"])

    def owner(self, date=None):
        """
        Return all owners (e.g. a subset of entities) on a specific date

        :param date: The date for the underlying positions snapshot, use today if not specified
        :return: entities
        """
        date = date or pd.Timestamp("today")
        ids = self.positions(date).index.get_level_values(level="Owner ID").unique()

        owners = self.entities().ix[ids][
            ["Name", "Type", "Ownership Type", "Top Level Owner ID", "Account Number", "Currency"]]

        # create an additional field...
        d = pd.Series({owner: list(owners[owners["Top Level Owner ID"] == str(owner)].index) for owner in owners.index})
        owners["Owned Accounts"] = d

        owners = owners.rename(columns={"Top Level Owner ID": "Owner"})
        return owners.set_index(["Type"], append=True)

    def products(self, date=None):
        """
        Return all products owned (e.g. a subset of entities) on a specific date

        :param date: The date for the underlying positions snapshot, use today if not specified
        :return: entities
        """
        date = date or pd.Timestamp("today")
        ids = self.positions(date).index.get_level_values(level="Owned ID").unique()
        return self.entities().ix[ids]
