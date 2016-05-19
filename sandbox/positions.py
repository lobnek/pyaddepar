import pandas as pd
from auth import aFirm, aKey, aSecret
from pyaddepar.graph.positions import Positions
from pyaddepar.reader import Reader
from sandbox.groups import Groups


if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = Reader(id=aFirm, key=aKey, secret=aSecret)

    # note that the positions are not a property as one could specify dates...
    position_graph = Positions(data=reader.positions())
    # the bipartite group graph
    group_graph = Groups(data=reader.groups)

    # {group1_id: [account1_id, ...], group2_id: ...}
    accounts = group_graph.owns
    print(accounts)

    # Loop over all groups
    for group_id, acc in accounts.items():
        print("*"*250)
        print(group_graph[group_id])
        print(acc)
        print(position_graph.owns(ids=acc))


