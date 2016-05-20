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
        self.__groups = [group_id for group_id in data.index.get_level_values(level="Group ID").unique()]
        self.__owns = pd.Series({group_id: list(self.__data.xs(group_id, level="Group ID").index) for group_id in self.__groups})
        self.__name = pd.Series({group_id: Groups.__verify_name(self.__data.xs(group_id, level="Group ID")["Group Name"])
                                 for group_id in self.__groups})

        assert len(self.__name.unique()) == len(self.__name)

    @property
    def groups(self):
        return self.__groups

    @property
    def name(self):
        """
        Series {group_id_i: name_i}
        :return:
        """
        return self.__name

    @property
    def group_id(self):
        """
        Series {name_i: group_id_i}
        :return:
        """
        return pd.Series({v: k for k, v in self.name.items()})

    @property
    def group_holdings(self):
        """
        Series {group_id_i : [member_1, ...]}
        :return:
        """
        #todo: I wish there would be a simple method to link from member_1 to account_1_of_member_1, account_2_of...
        #todo: This would make connecting with the transaction table a lot simpler
        return self.__owns