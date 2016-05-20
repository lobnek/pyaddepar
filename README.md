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
	
	from pyaddepar.reader import Reader
	
	if __name__ == '__main__':
		pd.set_option("display.width", 300)
		pd.set_option("display.max_rows", 300)
	
		# instantiate reader (e.g. wrapper of the addepar REST api)
		reader = Reader(id=aFirm, key=aKey, secret=aSecret)
	
		print(reader.groups)
	
		e = reader.entities()
		print(e)
		print(e.keys())
	
		t = reader.transactions()
		print(t.dtypes)
		print(t)




