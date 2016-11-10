import pandas as pd
from auth import aFirm, aKey, aSecret
from pyaddepar.preader import PReader


if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = PReader(id=aFirm, key=aKey, secret=aSecret)

    # our M. client
    group_id = "5481"

    # M owns a few accounts
    group = reader.groups[group_id]
    print("Group: {0}".format(reader.groups[group_id]))

    group_members = group.owns
    print("Group member: {0}".format(group_members))

    # Everything that is owned by the group members and other owners down the graph
    print(reader.positions(date=pd.Timestamp("2016-01-18")).edges(ids=group_members))
    print(reader.transactions.edges(ids=group_members))

