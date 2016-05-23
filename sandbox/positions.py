import pandas as pd
from auth import aFirm, aKey, aSecret
from pyaddepar.preader import PReader

if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = PReader(id=aFirm, key=aKey, secret=aSecret)

    # Loop over all groups
    for group_id, group in reader.groups.items():
        print("*" * 250)
        print(group_id)
        print(group)
        print(reader.positions(date=pd.Timestamp("today")).left(ids=group.owns))


