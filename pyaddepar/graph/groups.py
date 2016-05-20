import pandas as pd


class Groups(object):
    """
    Groups are described by a bipartite graph. With Group vs. Members. A member can be in multiple groups.
    A member can not be a group and a group can not be member of a different group.
    """
    @staticmethod
    def __verify_name(names):
        x = names[0]
        for name in names:
            assert name == x
        return x

    def __init__(self, data):
        self.__data = data
        self.__groups = [group for group in data.index.get_level_values(level="Group ID").unique()]
        self.__owns = pd.Series({group: list(self.__data.xs(group, level="Group ID").index) for group in self.__groups})
        self.__name = pd.Series({group: Groups.__verify_name(self.__data.xs(group, level="Group ID")["Group Name"])
                                 for group in self.__groups})

        assert len(self.__name.unique()) == len(self.__name)

    @property
    def ids(self):
        return self.__name

    @property
    def names(self):
        return pd.Series({v: k for k, v in self.ids.items()})

    @property
    def owns(self):
        return self.__owns

    def __repr__(self):
        return self.__data.to_string()
