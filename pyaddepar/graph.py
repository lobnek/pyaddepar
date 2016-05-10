import itertools


class PositionGraph(object):
    def __init__(self, positions):
        owner = positions.index.get_level_values(level="Owner ID").unique()
        self.__owner = {o: list(positions.xs(o, level="Owner ID", drop_level=True).index) for o in owner}

    def __owns(self, owner):
        # get a list of nodes that can be reached directly from a node
        if owner in self.__owner.keys():
            return [owner] + list(itertools.chain.from_iterable([self.__owns(o) for o in self.__owner[owner]]))
        else:
            return [owner]

    @property
    def owner_structure(self):
        """
        Returns a dictionary of pairs id: [list of ids]. Here id is the id of an owner and and the list of ids
        is the list of all assets/accounts/nodes reachable from id, e.g. everything the owner owns. This relationship
        may not be very direct. An owner may own an account. The account may own yet another account and the 2nd account
        may own a fund. With this construction we can reflect all of this and link the asset directly
        to the owner. The owner appers as a key but so do the two accounts...

        :return: big dictionary. Every owner is a key.
        """
        return {owner: self.__owns(owner) for owner in self.__owner.keys()}
