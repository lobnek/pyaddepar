import networkx as nx


class Groups(object):
    """
    Groups are described by a bipartite graph. With Group vs. Members. A member can be in multiple groups.
    A member can not be a group and a group can not be member of a different group.
    """
    def __init__(self, data):
        self.__data = data
        self.__dg = nx.DiGraph()

        for names, ids in data.iterrows():
            self.__dg.add_node(ids["Group ID"], attr_dict={"name": names[0]}, bipartite=0)
            self.__dg.add_node(ids["Member ID"], attr_dict={"name": names[1]}, bipartite=1)
            self.__dg.add_edge(ids["Group ID"], ids["Member ID"])

        self.__bottom_nodes, self.__top_nodes = nx.bipartite.sets(self.__dg)

    @property
    def groups(self):
        return self.__bottom_nodes

    @property
    def member(self):
        return self.__top_nodes

    def __getitem__(self, item):
        return self.__dg.node[item]

    def owns(self, id):
        return self.__dg.successors(id)

    def owned(self, id):
        return self.__dg.predecessors(id)

    def __repr__(self):
        return self.__data.to_string()

    def draw(self):
        pos = dict()
        pos.update((n, (1, 3*i)) for i, n in enumerate(self.groups))  # put nodes from X at x=1
        pos.update((n, (2, i)) for i, n in enumerate(self.member))  # put nodes from Y at x=2

        nx.draw_networkx_nodes(self.__dg, pos, nodelist=self.groups, node_color="b")
        nx.draw_networkx_nodes(self.__dg, pos, nodelist=self.member, node_color="r")
        nx.draw_networkx_edges(self.__dg, pos)


