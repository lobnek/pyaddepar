import networkx as nx
import pandas as pd


class PandasGraph(object):
    """
    Given a Pandas Dataframe, we can take two index-columns called left and right to create a graph G with edges from
    the 'left' to the 'right'.
    """
    def __init__(self, data, left="Owner ID", right="Owned ID"):
        """
        We create a graph based on two columns in the MultiIndex of a Pandas DataFrame.

        :param data: A pandas DataFrame with a MultiIndex.
        :param left: The name of the level for the starting nodes (e.g. we start all edges in them)
        :param right: The name of the level for the ending nodes (e.g. we end all edges in them)
        """
        self.__data = data.sortlevel(level=0)
        self.__dg = nx.DiGraph()
        self.__left = left
        self.__right = right

        graph = zip(data.index.get_level_values(level=left), data.index.get_level_values(level=right))

        for left_n, right_n in graph:
            self.__dg.add_node(left_n)
            self.__dg.add_node(right_n)
            self.__dg.add_edge(left_n, right_n)

    @property
    def data(self):
        return self.__data

    def __edge(self, left, right):
        return self.__data.xs([left, right], level=[self.__left, self.__right], drop_level=False)

    def edges(self, ids):
        """
        Return all edges reachable from a node described in the list ids.
        If A owns B and B owns C, we get[[A,B],[B,C]]
        """
        assert isinstance(ids, list)
        # all edges reachable from a list of nodes
        return pd.concat([pd.concat([self.__edge(e[0], e[1]) for e in nx.dfs_edges(self.__dg, id)]) for id in ids])
