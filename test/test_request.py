from unittest import TestCase

import pandas as pd
import requests_mock

from pyaddepar.request import Request, PortfolioType
import pandas.util.testing as pdt


class TestRequest(TestCase):
    def test_version(self):
        with requests_mock.mock() as m:
            r = Request(key="1", secret="1", id="maffay", company="maffay")
            m.get("https://maffay.addepar.com/api/v1/api_version", json={'a':'b'})
            y = r.version
            self.assertEqual(y, {'a':'b'})

    def test_auth(self):
        r = Request(key="a", secret="bb")
        self.assertEqual(r.auth, ("a", "bb"))

    def test_dicturl(self):
        x = Request().dicturl({"a":200,"b":"cc"})
        self.assertEqual(x, "a=200&b=cc")

    # def test_view(self):
    #     with requests_mock.mock() as m:
    #         m.get("https://petermaffay.addepar.com/api/v1/portfolio/views/10/results?portfolio_id=20&portfolio_type=entity&output_type=json&start_date=1978-11-12&end_date=1978-11-12", json={'a':'b'})
    #         x = Request().view(view_id=10, portfolio_id=20, portfolio_type=PortfolioType.ENTITY, start_date=pd.Timestamp("12-Nov-1978"), end_date=pd.Timestamp("12-Nov-1978"))
    #         self.assertEqual(x, {'a': 'b'})

    def test_view_csv(self):
        with requests_mock.mock() as m:
            xxx = pd.DataFrame(index=["x","y"], columns=["a"], data=[[4], [5]])
            xxx.index.name = "Peter"

            m.get("https://petermaffay.addepar.com/api/v1/portfolio/views/10/results?portfolio_id=20&portfolio_type=entity&output_type=csv&start_date=1978-11-12&end_date=1978-11-12", text=xxx.to_csv())
            x = Request().view_csv(view_id=10, portfolio_id=20, portfolio_type=PortfolioType.ENTITY, start_date=pd.Timestamp("12-Nov-1978"), end_date=pd.Timestamp("12-Nov-1978"))

            pdt.assert_frame_equal(x, xxx.reset_index())

    def test_users(self):
        with requests_mock.mock() as m:
            m.get("https://petermaffay.addepar.com/api/v1/users", json={"data": [{"id": "1", "attributes": {"a": 2.0, "b": 3.0}}], "links": {"next": None}})
            x = {key: attr for key, attr in Request().users}
            self.assertDictEqual(x, {"1": {"a": 2.0, "b": 3.0}})

    def test_user_id(self):
        with requests_mock.mock() as m:
            m.get("https://petermaffay.addepar.com/api/v1/users/1",
                  json={"data": {"id": "1", "attributes": {"a": 2.0, "b": 3.0}}})
            x = Request().user(id=1)
            self.assertDictEqual(x, {"a": 2.0, "b": 3.0})

    def test_entities(self):
        with requests_mock.mock() as m:
            m.get("https://petermaffay.addepar.com/api/v1/entities", json={"data": [{"id": "1", "attributes": {"a": 2.0, "b": 3.0}}], "links": {"next": None}})
            x = {key: attr for key, attr in Request().entities}
            self.assertDictEqual(x, {"1": {"a": 2.0, "b": 3.0}})

    def test_entity_id(self):
        with requests_mock.mock() as m:
            m.get("https://petermaffay.addepar.com/api/v1/entities/1", json={"data": {"id": "1", "attributes": {"a": 2.0, "b": 3.0}}})
            x = Request().entity(entity=1)
            self.assertDictEqual(x, {"a": 2.0, "b": 3.0})

