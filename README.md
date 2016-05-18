# pyaddepar

Addepar has recently released a REST api. In this project we wrap this api for Python users.


Installation
------------
    pip install git+http://github.com/lobnek/pyaddepar.git
    
Authentication
--------------

Create a file auth.py using the following template:

    # Addepar auth details
    aFirm = "123"
    aKey = "your key"
    aSecret = "your secret"
    figiKey = "Go and get me free from https://www.openfigi.com/user/signup"
    
    
Usage
-----

Here's a little fragment:

    from auth import aFirm, aKey, aSecret
    import pandas as pd
    
    if __name__ == '__main__':
        pd.set_option("display.width", 300)
    
        from pyaddepar.reader import Reader
    
        # instantiate reader (e.g. wrapper of the addepar REST api)
        reader = Reader(id=aFirm, key=aKey, secret=aSecret)
    
        # all positions currently in the database
        print(reader.positions())
    
        # cross section across rows with Owner ID == 804328
        print(reader.positions().xs(804328, level="Owner ID"))
    
        # cross section across rows with Owned ID == 867344
        print(reader.positions().xs(867344, level="Owned ID"))
    
        # all current owners
        print(reader.owner())
    
        # all current products
        print(reader.products())
    
        # all contacts, note that this is a property rather than a method
        print(reader.contacts)
    
        # all groups, their members (and their IDs)
        print(reader.groups)



