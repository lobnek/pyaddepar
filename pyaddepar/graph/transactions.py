class Transactions(object):
    """
    Transactions are described by a bipartite graph. With Owner vs. Owned. Only accounts can make transactions.
    """
    def __init__(self, data):
        self.__data = data.sortlevel(level=0)

    def transactions(self, id=None, date=None):
        """ List of all edges reachable from node id """
        p = self.__data
        if date:
            p = p.xs(date, level='Date', drop_level=False)

        if id:
            p = p.xs(id, level='Owner ID', drop_level=False)

        return p
