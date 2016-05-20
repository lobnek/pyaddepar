import pandas as pd
from auth import aFirm, aKey, aSecret
from pyaddepar.reader import Reader
from pyaddepar.graph.groups import Groups

if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = Reader(id=aFirm, key=aKey, secret=aSecret)

    x = Groups(data=reader.groups)
    print(x.name)
    print(x.group_id)
    print(x.group_holdings)
    print(x.group_holdings["5098"])
    print(x.group_holdings[x.group_id[".LWM Group"]])

