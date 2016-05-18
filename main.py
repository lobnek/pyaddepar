from auth import aFirm, aKey, aSecret
import pandas as pd
import logging
from pyaddepar.graph.groups import Groups
from pyaddepar.graph.positions import Positions

from pyaddepar.reader import Reader

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pyaddepar")

# the existing requests logger can be controlled here...
logging.getLogger("requests").setLevel(level=logging.WARNING)


if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = Reader(id=aFirm, key=aKey, secret=aSecret, logger=logger)

    print(reader.contacts)
    print(reader.groups)
    g = Groups(reader.groups)
    p = Positions(reader.positions())

    #graph = PositionGraph(reader.positions())
    #print(graph.owner_structure)

    #e = reader.entities()
    #print(e)
    #print(e.keys())
    #assert False


    # p = reader.positions()
    # print(p)
    # print(p.dtypes)
    # assert False
    #
    #
    # p = reader.positions()
    # print(p)
    # #print(p.loc(axis=0)["864551", :])
    # #print(p.loc(axis=0)[:, "882501"])
    #
    # e = reader.entities()
    # print(e)
    # print(e.dtypes)
    #
    # t = reader.transactions()
    # print(t.dtypes)
    # print(t)
