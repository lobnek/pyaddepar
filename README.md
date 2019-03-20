# pyaddepar
Addepar has recently released a REST api. In this project we wrap this api for Python users.


Installation
------------
    pip install git+http://github.com/lobnek/pyaddepar.git
    
Authentication
--------------

Create a file .config using the following template:

    # Addepar auth details
    AFIRM=123
    AKEY=123
    ASECRET=123
    COMPANY=AAA

    
Usage
-----

Here's a little fragment:


    from pyaddepar.request import Request
    print(Request().version)

    print(Request().entity())

    print(Request().group())

    print(Request().entity(id=123))

    print(Request().group(id=123))

All this simple requests rely on the

    def get(self, request):
        r = "https://{company}.addepar.com/api/v1/{request}".format(request=request, company=self.__company)
        r = requests.get(r, auth=self.auth, headers=self.headers)
        assert r.ok, "Invalid response. Statuscode {}".format(r.status_code)
        # it's more standard to return r rather than r.json(), hence client can check return code...
        return r
