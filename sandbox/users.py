import pprint

from pyaddepar.request import Request

if __name__ == '__main__':
    for key, entity in Request().users().items():
        print(key)
        pprint.pprint(entity)

    print(Request().users(id=429609))

    for key, entity in Request().entity().items():
        print(key)
        pprint.pprint(entity)

    print(Request().entity(id=2395977))

    #for key, entity in Request().group().items():
    #    print(key)
    #    pprint.pprint(entity)

    #print(Request().group(id=5483))



