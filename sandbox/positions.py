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
    positions = Positions(data=reader.positions())
    # the bipartite group graph
    groups = Groups(data=reader.groups)

    # Loop over all groups
    for group_id in groups.groups:
        print("*" * 250)
        print(group_id)
        print(groups.name[group_id])
        accounts = groups.group_holdings[group_id]
        print(positions.owns(ids=accounts))


