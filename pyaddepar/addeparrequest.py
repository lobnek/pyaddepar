import json
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


class AddeparRequest(object):
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
        return {"Accept": "*/*", "Addepar-Firm": self.id, "content-type": "application/vnd.api+json"}

    @staticmethod
    def dicturl(d):
        return '&'.join(["{key}={value}".format(key=key, value=value) for key, value in d.items()])

    def get(self, request):
        request = "https://{company}.addepar.com/api{request}".format(request=request, company=self.company)
        self.logger.debug("Request: {request}, Headers: {headers}".format(request=request, headers=self.headers))

        r = requests.get(request, auth=(self.key, self.secret), headers=self.headers)
        assert r.ok, "Invalid response. Statuscode {code}. Query: {x}".format(code=r.status_code, x=request)
        return r

    def post(self, data, request="entities"):
        r = "https://{company}.addepar.com/api/v1/{request}".format(request=request, company=self.company)
        self.logger.debug("Request: {request}, Headers: {headers}".format(request=r, headers=self.headers))
        r = requests.post(r, auth=(self.key, self.secret), headers=self.headers, data=json.dumps(data))
        assert r.ok, "Invalid response. Statuscode {}".format(r.status_code)
        return r

    def delete(self, entity):
        assert entity
        r = "https://{company}.addepar.com/api/v1/entities/{entity}".format(company=self.company, entity=entity)
        return requests.delete(r, auth=(self.key, self.secret), headers=self.headers)

    @property
    def version(self):
        return self.get("/v1/api_version").json()

    def view_csv(self, view_id, portfolio_id, portfolio_type, start_date=pd.Timestamp("today"),
                 end_date=pd.Timestamp("today")):

        assert isinstance(portfolio_type, PortfolioType)

        param = AddeparRequest.dicturl({"portfolio_id": portfolio_id, "portfolio_type": portfolio_type.value,
                                 "output_type": OutputType.CSV.value, "start_date": start_date.strftime("%Y-%m-%d"),
                                 "end_date": end_date.strftime("%Y-%m-%d"), "addepar_firm": self.id})

        request = "/v1/portfolio/views/{view}/results?{param}".format(view=view_id, param=param)

        self.logger.debug("Request: {request}".format(request=request))
        return pd.read_csv(io.BytesIO(self.get(request=request).content))

    def transaction_csv(self, view_id, portfolio_id, portfolio_type, start_date=pd.Timestamp("today"),
                        end_date=pd.Timestamp("today")):

        assert isinstance(portfolio_type, PortfolioType)

        param = AddeparRequest.dicturl({"portfolio_id": portfolio_id, "portfolio_type": portfolio_type.value,
                                 "output_type": OutputType.CSV.value, "start_date": start_date.strftime("%Y-%m-%d"),
                                 "end_date": end_date.strftime("%Y-%m-%d"), "addepar_firm": self.id})

        request = "/v1/transactions/views/{view}/results?{param}".format(view=view_id, param=param)

        self.logger.debug("Request: {request}".format(request=request))
        return pd.read_csv(io.BytesIO(self.get(request=request).content))

    def entities(self, link="/v1/entities", modeltype=None):
        while link:
            a = self.get(link).json()
            for x in a["data"]:
                if modeltype:
                    if x["model_type"] == modeltype:
                        yield x["id"], AttrDict(x["attributes"])
                else:
                    yield x["id"], AttrDict(x["attributes"])
            link = a["links"]["next"]

    @property
    def users(self):
        return self.entities(link="/v1/users")

    @property
    def groups(self):
        return self.entities(link="/v1/groups")

    def group(self, id):
        return AttrDict(self.get("/v1/groups/{id}".format(id=id)).json()["data"]["attributes"])

    def user(self, id):
        return AttrDict(self.get("/v1/users/{id}".format(id=id)).json()["data"]["attributes"])

    def entity(self, id):
        return AttrDict(self.get("/v1/entities/{id}".format(id=id)).json()["data"]["attributes"])

    def members(self, id):
        for row in self.get("/v1/groups/{id}/relationships/members".format(id=id)).json()["data"]:
            yield row["id"]

    @property
    def persons(self):
        return self.entities(link="/v1/entities", modeltype="PERSON_NODE")

    @property
    def options(self):
        return self.entities(link="/v1/entities", modeltype="OPTION")
