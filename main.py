from auth import aFirm, aKey, aSecret
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pyaddepar")

# the existing requests logger can be controlled here...
logging.getLogger("requests").setLevel(level=logging.WARNING)


if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)
    from pyaddepar.reader import Reader

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = Reader(id=aFirm, key=aKey, secret=aSecret, logger=logger)

    # print the reader __repr__()
    print(reader)

    # print the contacts
    print(reader.contacts)
    print(reader.contacts.dtypes)

    # all positions currently in the database
    p = reader.positions()
    print(p)
    print(p.dtypes)

    # cross section across rows with Owner ID == 804328
    print(reader.positions().xs(804328, level="Owner ID"))

    # cross section across rows with Owned ID == 867344
    print(reader.positions().xs(867344, level="Owned ID"))

    e = reader.entities()
    print(e)
    print(e.dtypes)


    # all current owners
    o = reader.owner()
    print(o)
    print(o.dtypes)


    # all current products
    p = reader.products()
    print(p)
    print(p.dtypes)

    # all contacts, note that this is a property rather than a method
    print(reader.contacts)

    # all groups, their members (and their IDs)
    print(reader.groups)

    t = reader.transactions()
    print(t.dtypes)
    print(t)