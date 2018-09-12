import logging
import os
from enum import Enum

import pandas as pd
import requests


class OutputType(Enum):
    CSV = "csv"
    JSON = "json"
    TSV = "tsv"
    XLSX = "xlsx"


class PortfolioType(Enum):
    GROUP = "group"
    FIRM = "firm"
    ENTITY = "entity"


def addepar2frame(json, index="name"):
    x = json["data"]["attributes"]["total"]["children"]
    frame = pd.DataFrame({i:  {**{index: a[index]}, **a["columns"]} for i,a in enumerate(x)}).transpose()
    names = {a["key"]: a["display_name"] for a in json["meta"]["columns"]}
    return frame.rename(columns=lambda x: names[x] if  x in names.keys() else x)


class Request(object):
    def __init__(self, key=None, secret=None, id=None, company=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.key = key or os.environ["AKEY"]
        self.secret = secret or os.environ["ASECRET"]
        self.id = id or os.environ["AFIRM"]
        self.company = company or os.environ["COMPANY"]

    @property
    def auth(self):
        return self.key, self.secret

    @property
    def headers(self):
        return {"content-type": "application/vnd.api+json", "Addepar-Firm": self.id}

    def get(self, request):
        h = self.headers

        r = "https://{company}.addepar.com/api/v1/{request}".format(request=request, company=self.company)
        self.logger.debug("Request: {request}, Headers: {headers}".format(request=r, headers=h))
        r = requests.get(r, auth=(self.key, self.secret), headers=h)
        assert r.ok, "Invalid response. Statuscode {}".format(r.status_code)
        return r

    @property
    def version(self):
        return self.get("api_version")

    def view(self, view_id, portfolio_id, portfolio_type, start_date=(pd.Timestamp("today")),
                     end_date=pd.Timestamp("today")):

        def __dict(d):
            return '&'.join(["{key}={value}".format(key=key, value=value) for key, value in d.items()])

        assert isinstance(portfolio_type, PortfolioType)

        request = "portfolio/views/{view}/results?".format(view=view_id) + \
                  __dict({"portfolio_id": portfolio_id,
                          "portfolio_type": portfolio_type.value,
                          "output_type": OutputType.JSON.value,
                          "start_date": start_date.strftime("%Y-%m-%d"),
                          "end_date": end_date.strftime("%Y-%m-%d")})

        self.logger.debug("Request: {request}".format(request=request))
        return self.get(request=request).json()

    def entity(self, id=None):
        if id:
            return self.get("entities/{id}".format(id=id)).json()
        else:
            return self.get("entities").json()

    def group(self, id=None):
        if id:
            return self.get("groups/{id}/members".format(id=id))
        else:
            return self.get("groups")

    def post_file(self, new_name, name):
        #h = {"Addepar-Firm": self.id}
        r = "https://{company}.addepar.com/api/v1/{request}".format(request="files", company=self.company)

        files = {'file': (new_name, open(name, "rb"))}
        r = requests.post(r, auth=self.auth, headers=self.headers, files=files)

        assert r.ok, "Invalid response. Statuscode {}".format(r.status_code)
        return r.json()["data"]

    def files(self, id=None):
        if id:
            return self.get("files/{id}".format(id=id)).json()
        else:
            x = self.get("files").json()
            return {a["id"] : a for a in x["data"]}

    def file_download(self, id, file=None):
        r =  self.get("files/{id}/download".format(id=id))
        if file:
            with open(file, "wb") as f:
                f.write(r.content)

    def file_groups(self, id):
        return self.get("files/{id}/associated_groups".format(id=id)).json()

    def file_entities(self, id):
        return self.get("files/{id}/associated_entities".format(id=id)).json()
    #GET / v1 / files /: file - id / associated_groups

    def file_delete(self, id):
        #r = "https://{company}.addepar.com/api/v1/{request}".format(request=request, company=self.company)
        #self.logger.debug("Request: {request}, Headers: {headers}".format(request=r, headers=h))
        #DELETE / v1 / files /: file - id
        r = requests.delete("https://{company}.addepar.com/api/v1/files/{id}".format(id=id, company=self.company),  auth=self.auth, header=self.headers)
        assert r.ok, "Invalid response. Statuscode {}".format(r.status_code)
        #r = requests.get(r, auth=(self.key, self.secret), headers=h)


if __name__ == '__main__':
    y = Request().post_file(new_name="test10.csv", name="/data/report.csv")
    Request().file_delete(id=y["id"])
    Request().file_download(id=y["id"], file="/data/graph8.csv")

