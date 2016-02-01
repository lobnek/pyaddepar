from auth import aFirm, aKey, aSecret
import pandas as pd

if __name__ == '__main__':
    pd.set_option("display.width", 300)

    from pyaddepar.reader import Reader

    reader = Reader(id=aFirm, key=aKey, secret=aSecret)

    print(reader.positions())
    print(reader.positions().ix["804328"])
    print(reader.positions().xs("804328", level="Owner ID"))
    print(reader.positions().xs("867344", level="Owned ID"))

    print(reader.owner)
    print(reader.products)
    print(reader.transactions())
    assert False

    # print(reader.entities())


    # p = reader.positions()
    # print(p.keys())
    # print(p)

    # print(reader.entities())

    print(reader.portfolio())
