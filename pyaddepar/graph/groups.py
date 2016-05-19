import networkx as nx


class Groups(object):
    """
    Groups are described by a bipartite graph. With Group vs. Members. A member can be in multiple groups.
    A member can not be a group and a group can not be member of a different group.
    """
    def __init__(self, data):
        self.__data = data
        self.__dg = nx.DiGraph()

        for ids, x in data.iterrows():
            self.__dg.add_node(ids[0], attr_dict={"name": x["Group Name"]}, bipartite=0)
            self.__dg.add_node(ids[1], attr_dict={"name": x["Member Name"]}, bipartite=1)
            self.__dg.add_edge(ids[0], ids[1])

        self.__bottom_nodes, self.__top_nodes = nx.bipartite.sets(self.__dg)

    @property
    def ids(self):
        return {group: self[group]["name"] for group in self.__bottom_nodes}

    @property
    def names(self):
        return {self[group]["name"]: group for group in self.__bottom_nodes}

    def __getitem__(self, id):
        return self.__dg.node[id]

    @property
    def owns(self):
        return {group: self.__dg.successors(group) for group in self.__bottom_nodes}

    @property
    def owned(self):
        return {group: self.__dg.predecessors(group) for group in self.__top_nodes}

    def __repr__(self):
        return self.__data.to_string()


