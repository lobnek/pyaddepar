import networkx as nx
import pandas as pd


class PandasGraph(object):
    def __init__(self, data):
        self.__data = data.sortlevel(level=0)
        self.__dg = nx.DiGraph()

        for ids in data.index:
            self.__dg.add_node(ids[0])
            self.__dg.add_node(ids[1])
            self.__dg.add_edge(ids[0], ids[1])

    @property
    def data(self):
        return self.__data

    def __edge(self, owner, owns):
        return self.__data.xs([owner, owns], level=["Owner ID", "Owned ID"], drop_level=False)

    def __edges(self, id):
        """ List of all edges reachable from node id """
        return pd.concat([self.__edge(owner=e[0], owns=e[1]) for e in nx.dfs_edges(self.__dg, id)], axis=0)

    def left(self, ids):
        assert isinstance(ids, list)
        # all edges reachable from a list of nodes
        return pd.concat([self.__edges(id) for id in ids], axis=0)
