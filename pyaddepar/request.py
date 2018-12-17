import logging
import os
from enum import Enum

import pandas as pd
import requests
import io


class OutputType(Enum):
    CSV = "csv"
    JSON = "json"
    TSV = "tsv"
    XLSX = "xlsx"


class PortfolioType(Enum):
    GROUP = "group"
    FIRM = "firm"
    ENTITY = "entity"


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


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

    @staticmethod
    def dicturl(d):
        return '&'.join(["{key}={value}".format(key=key, value=value) for key, value in d.items()])

    def get(self, request):
        r = "https://{company}.addepar.com/api{request}".format(request=request, company=self.company)
        self.logger.debug("Request: {request}, Headers: {headers}".format(request=r, headers=self.headers))
        r = requests.get(r, auth=(self.key, self.secret), headers=self.headers)
        assert r.ok, "Invalid response. Statuscode {}".format(r.status_code)
        return r

    @property
    def version(self):
        return self.get("/v1/api_version").json()

    # def view(self, view_id, portfolio_id, portfolio_type, start_date=pd.Timestamp("today"),
    #          end_date=pd.Timestamp("today")):
    #
    #     assert isinstance(portfolio_type, PortfolioType)
    #
    #     param = Request.dicturl({"portfolio_id": portfolio_id, "portfolio_type": portfolio_type.value,
    #                              "output_type": OutputType.JSON.value, "start_date": start_date.strftime("%Y-%m-%d"),
    #                              "end_date": end_date.strftime("%Y-%m-%d")})
    #
    #     request = "portfolio/views/{view}/results?{param}".format(view=view_id, param=param)
    #
    #     self.logger.debug("Request: {request}".format(request=request))
    #     return self.get(request=request).json()

    def view_csv(self, view_id, portfolio_id, portfolio_type, start_date=pd.Timestamp("today"),
                 end_date=pd.Timestamp("today")):

        assert isinstance(portfolio_type, PortfolioType)

        param = Request.dicturl({"portfolio_id": portfolio_id, "portfolio_type": portfolio_type.value,
                                 "output_type": OutputType.CSV.value, "start_date": start_date.strftime("%Y-%m-%d"),
                                 "end_date": end_date.strftime("%Y-%m-%d")})

        request = "/v1/portfolio/views/{view}/results?{param}".format(view=view_id, param=param)

        self.logger.debug("Request: {request}".format(request=request))
        return pd.read_csv(io.BytesIO(self.get(request=request).content))

    def entity(self, entity):
        #print(self.get("/v1/entities/{id}".format(id=entity)).json())
        return AttrDict(self.get("/v1/entities/{id}".format(id=entity)).json()["data"]["attributes"])

    @property
    def entities(self):
        link = "/v1/entities"
        while link:
            a = self.get(link).json()
            for x in a["data"]:
                yield x["id"], AttrDict(x["attributes"])
            link = a["links"]["next"]

    @property
    def users(self):
        link = "/v1/users"
        while link:
            a = self.get(link).json()
            for x in a["data"]:
                yield x["id"], AttrDict(x["attributes"])
            link = a["links"]["next"]

    @property
    def groups(self):
        link = "/v1/groups"
        while link:
            a = self.get(link).json()
            for x in a["data"]:
                yield x["id"], AttrDict(x["attributes"])
            link = a["links"]["next"]

    #def group(self, id=None):
    #    if id:
    #        return self.get("groups/{id}/members".format(id=id)).json()["data"]
    #    else:
    #        return {a["id"]: AttrDict(a["attributes"]) for a in self.get("groups").json()["data"]}

    def user(self, id):
        #if id:
        return AttrDict(self.get("/v1/users/{id}".format(id=id)).json()["data"]["attributes"])
        #else:
        #    link = "/v1/users"
        #    #while link:
        #        a = self.get(link).json()
        #        for x in a["data"]:
        #            yield x["id"], AttrDict(x["attributes"])
        #        link = a["links"]["next"]

    # def post_file(self, new_name, name):
    #     # h = {"Addepar-Firm": self.id}
    #     r = "https://{company}.addepar.com/api/v1/{request}".format(request="files", company=self.company)
    #
    #     files = {'file': (new_name, open(name, "rb"))}
    #     r = requests.post(r, auth=self.auth, headers=self.headers, files=files)
    #
    #     assert r.ok, "Invalid response. Statuscode {}".format(r.status_code)
    #     return r.json()["data"]
    #
    # def files(self, id=None):
    #     if id:
    #         return self.get("files/{id}".format(id=id)).json()
    #     else:
    #         x = self.get("files").json()
    #         return {a["id"]: a for a in x["data"]}
    #
    # def file_download(self, id, file=None):
    #     r = self.get("files/{id}/download".format(id=id))
    #     if file:
    #         with open(file, "wb") as f:
    #             f.write(r.content)
    #
    # def file_groups(self, id):
    #     return self.get("files/{id}/associated_groups".format(id=id)).json()
    #
    # def file_entities(self, id):
    #     return self.get("files/{id}/associated_entities".format(id=id)).json()
    #
    # # GET / v1 / files /: file - id / associated_groups
    #
    # def file_delete(self, id):
    #     # r = "https://{company}.addepar.com/api/v1/{request}".format(request=request, company=self.company)
    #     # self.logger.debug("Request: {request}, Headers: {headers}".format(request=r, headers=h))
    #     # DELETE / v1 / files /: file - id
    #     r = requests.delete("https://{company}.addepar.com/api/v1/files/{id}".format(id=id, company=self.company),
    #                         auth=self.auth, header=self.headers)
    #     assert r.ok, "Invalid response. Statuscode {}".format(r.status_code)
    #     # r = requests.get(r, auth=(self.key, self.secret), headers=h)


