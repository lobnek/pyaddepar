import networkx as nx
import pandas as pd


class Positions(object):
    """
    Positions are not a bipartite graph. An owner can be owned by a different owner. We model this as a directed graph.
    """
    def __init__(self, data):
        self.__data = data.sortlevel(level=0)
        self.__dg = nx.DiGraph()

        for ids, d in data.iterrows():
            self.__dg.add_node(ids[0])
            self.__dg.add_node(ids[1])
            self.__dg.add_edge(ids[0], ids[1], attr_dict=d.to_dict())

    @property
    def data(self):
        return self.__data

    def __edge(self, owner, owns):
        return self.__data.ix[[(owner, owns)]]

    def __edges(self, id):
        """ List of all edges reachable from node id """
        return pd.concat([self.__edge(owner=e[0], owns=e[1]) for e in nx.dfs_edges(self.__dg, id)], axis=0)

    def owns(self, ids):
        assert isinstance(ids, list)
        # all edges reachable from a list of nodes
        return pd.concat([self.__edges(id) for id in ids], axis=0)

    def left(self, ids):
        """
        The list of all bottom nodes reachable from a given list of nodes
        """
        return list(self.owns(ids).index.get_level_values(level="Owner ID").unique())

    def __repr__(self):
        return self.__data.to_string()

