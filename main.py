from auth import aFirm, aKey, aSecret
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pyaddepar")

# the existing requests logger can be controlled here...
logging.getLogger("requests").setLevel(level=logging.WARNING)


if __name__ == '__main__':
    pd.set_option("display.width", 300)

    from pyaddepar.reader import Reader

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = Reader(id=aFirm, key=aKey, secret=aSecret, logger=logger)


    # print the reader __repr__()
    print(reader)

    print(reader.transactions())
    # all positions currently in the database
    print(reader.positions())

    # cross section across rows with Owner ID == 804328
    print(reader.positions().xs("804328", level="Owner ID"))

    # cross section across rows with Owned ID == 867344
    print(reader.positions().xs("867344", level="Owned ID"))

    # all current owners
    print(reader.owner())

    # all current products
    print(reader.products())

    # all contacts, note that this is a property rather than a method
    print(reader.contacts)

    # all groups, their members (and their IDs)
    print(reader.groups)


