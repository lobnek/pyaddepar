# pyaddepar
[![Action Status](https://github.com/lobnek/pyaddepar/workflows/CI/badge.svg)](https://github.com/lobnek/pyaddepar/actions/)


Some utility code for interacting with addepar. For more information on addepar please check out
https://addepar.com/.

## Installing pyaddepar
Install with pip
```
pip install pyaddepar
```

    
## AddeparRequest
AddeparRequest is a class hiding the management of your key(s), the pagination of requests and conversion of your results to standard pandas containers.

```
import pandas as pd
from pyaddepar.addeparrequest import AddeparRequest

if __name__ == '__main__':
    r = AddeparRequest(key=..., secret=..., id=..., company=...)
    today = pd.Timestamp("today")

    for key, entity in r.options:
        expiry = pd.Timestamp(entity["expiration_date"])
        if expiry >= today:
            print(expiry)
            print(entity)
            print(entity["option_type"])
            print(entity["node_strike_price"])

            print((expiry-today).days/365.0)

```
    
## Settings.cfg
We recommend to define a configuration file `(*.cfg)` containing

ADDEPAR = {"key":"A",
           "secret":"B",
           "id":"maffay",
           "company":"maffay"
          }

## Flask-Addepar
A Flask extension that provides integration with Addepar. In particular this flask extension provides
management of the your AddeparRequests. You can use configuration files such as settings.cfg to follow standard flask practices.
The configuration is easy, just fetch the extension:

```
from flask import Flask

from pyaddepar.flask_addepar import addepar

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_pyfile('config/settings.cfg')
    addepar.init_app(app)
    
    with app.app_context():
        for key, entity in addepar.request.entities():
            print(key)
            print(entity)

```

