from pyaddepar.graph.groups import Groups
from pyaddepar.graph.pandasgraph import PandasGraph
from pyaddepar.reader import Reader


class PReader(object):
    def __init__(self, id, key, secret, logger=None):
        self.__reader = Reader(id=id, key=key, secret=secret, logger=logger)

        self.__groups = Groups(data=self.__reader.groups)
        self.__transactions = PandasGraph(data=self.__reader.transactions())

        # self.__transactions.edge(owner="863621", owns="840896")

        # I have to use the positions to find out that 804361 also owns 804359
        # This is a bit of a drawback

        # get todays positions
        # self.__positions = Positions(data=self.__reader.positions())
        # self.__structure = self.__positions.owner

    #@property
    #def ownerstructure(self):
    #    return self.__structure

    @property
    def groups(self):
        return self.__groups

    @property
    def transactions(self):
        return self.__transactions

    def positions(self, date=None):
        return PandasGraph(data=self.__reader.positions(date=date))
