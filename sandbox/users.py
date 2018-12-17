import pprint

import pandas as pd

from pyaddepar.request import Request

if __name__ == '__main__':
    #for key, entity in Request().users().items():
    #    print(key)
    #    pprint.pprint(entity)

    #print(Request().users(id=429609))

    #for key, entity in Request().entity().items():
    #    print(key)
        #pprint.pprint(entity)
    print(pd.DataFrame({key: attr for key,attr in Request().entity()}).transpose())




    #pprint.pprint(Request().entity(id=4587126))
    #pprint.pprint(Request().entity(id=812750))
    #for key, entity in Request().group().items():
    #    print(key)
    #    pprint.pprint(entity)

    #print(Request().group(id=5483))



