import networkx as nx


class Positions(object):
    """
    Groups are described by a bipartite graph. With Group vs. Members. A member can be in multiple groups.
    A member can not be a group and a group can not be member of a different group.
    """

    def __init__(self, data):
        self.__data = data
        self.__dg = nx.DiGraph()
        print(data)

        for ids, d in data.iterrows():
            self.__dg.add_node(ids[0])
            self.__dg.add_node(ids[1])
            self.__dg.add_edge(ids[0], ids[1], attr_dict=d.to_dict())

    def __getitem__(self, item):
        return self.__dg.node[item]

    def owns(self, id):
        return self.__dg.successors(id)

    def owned(self, id):
        return self.__dg.predecessors(id)

    @property
    def nodes(self):
        return self.__dg.nodes()

    def edge(self, id_owner, id_owns):
        return self.__dg[id_owner][id_owns]

    @property
    def reachable(self):
        return {node: list(nx.dfs_postorder_nodes(self.__dg, node)) for node in self.nodes}

    @property
    def edges(self):
        return {node: [edge for edge in nx.dfs_edges(self.__dg, node)] for node in self.nodes}

    def __repr__(self):
        return self.__data.to_string()
