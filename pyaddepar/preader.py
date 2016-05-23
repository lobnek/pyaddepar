from pyaddepar.graph.groups import Groups
from pyaddepar.graph.positions import Positions
from pyaddepar.graph.transactions import Transactions
from pyaddepar.reader import Reader


class PReader(object):
    def __init__(self, id, key, secret, logger=None):
        self.__reader = Reader(id=id, key=key, secret=secret, logger=logger)

        self.__groups = Groups(data=self.__reader.groups)
        self.__transactions = Transactions(data=self.__reader.transactions())

    @property
    def groups(self):
        return self.__groups

    @property
    def transactions(self):
        return self.__transactions

    def positions(self, date=None):
        return Positions(data=self.__reader.positions(date=date))
