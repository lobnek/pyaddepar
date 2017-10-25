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


class Request(object):
    def __init__(self, key=None, secret=None, id=None, company=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.key = key or os.environ["AKEY"]
        self.secret = secret or os.environ["ASECRET"]
        self.id = id or os.environ["AFIRM"]
        self.company = company or os.environ["COMPANY"]

    @property
    def auth(self):
        return (self.key, self.secret)

    @property
    def headers(self):
        return {"content-type": "application/vnd.api+json", "Addepar-Firm": self.id}

    def get(self, request, headers=None):
        if headers:
            h = {**self.headers, **headers}
        else:
            h = self.headers

        r = "https://{company}.addepar.com/api/v1/{request}".format(request=request, company=self.company)
        self.logger.debug("Request: {request}, Headers: {headers}".format(request=r, headers=h))
        r = requests.get(r, auth=(self.key, self.secret), headers=h)
        assert r.ok, "Invalid response. Statuscode {}".format(r.status_code)
        return r.json()

    @property
    def version(self):
        return self.get("api_version").json()

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

        return self.get(request=request)

    def entity(self, id=None):
        if id:
            return self.get("entities/{id}".format(id=id))
        else:
            return self.get("entities")

    def group(self, id=None):
        if id:
            return self.get("groups/{id}/members".format(id=id))
        else:
            return self.get("groups")
