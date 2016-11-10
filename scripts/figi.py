#!/usr/bin/env python
import os
from pyaddepar.figi import figi

if __name__ == '__main__':
    figiKey = os.environ["FIGIKEY"]
    print(figi(idValue="CARSECC", idType="TICKER", openfigi_apikey=figiKey))
    print(figi(idValue="BBG000CBHLD2", idType="ID_BB_GLOBAL", openfigi_apikey=figiKey))