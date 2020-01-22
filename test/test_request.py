from unittest.mock import patch

import pandas as pd
import pandas.util.testing as pdt

from pyaddepar.request import Request, PortfolioType, AttrDict


class TestRequest(object):
    def test_version(self, requests_mock):
        r = Request(key="1", secret="1", id="maffay", company="maffay")
        requests_mock.get("https://maffay.addepar.com/api/v1/api_version", json={'a': 'b'})
        y = r.version
        assert y == {'a': 'b'}

    def test_auth(self):
        r = Request(key="a", secret="bb")
        assert r.auth == ("a", "bb")

    def test_dicturl(self):
        x = Request().dicturl({"a": 200, "b": "cc"})
        assert x == "a=200&b=cc"

    def test_view_csv(self, requests_mock):
        xxx = pd.DataFrame(index=["x", "y"], columns=["a"], data=[[4], [5]])
        xxx.index.name = "Peter"

        requests_mock.get(
            "https://petermaffay.addepar.com/api/v1/portfolio/views/10/results?portfolio_id=20&portfolio_type=entity&output_type=csv&start_date=1978-11-12&end_date=1978-11-12",
            text=xxx.to_csv())
        x = Request().view_csv(view_id=10, portfolio_id=20, portfolio_type=PortfolioType.ENTITY,
                               start_date=pd.Timestamp("12-Nov-1978"), end_date=pd.Timestamp("12-Nov-1978"))

        pdt.assert_frame_equal(x, xxx.reset_index())

    def test_users(self, requests_mock):
        requests_mock.get("https://petermaffay.addepar.com/api/v1/users",
                          json={"data": [{"id": "1", "attributes": {"a": 2.0, "b": 3.0}}], "links": {"next": None}})
        x = {key: attr for key, attr in Request().users}
        assert x == {"1": {"a": 2.0, "b": 3.0}}

    def test_user_id(self, requests_mock):
        requests_mock.get("https://petermaffay.addepar.com/api/v1/users/1",
                          json={"data": {"id": "1", "attributes": {"a": 2.0, "b": 3.0}}})
        x = Request().user(id=1)
        assert x == {"a": 2.0, "b": 3.0}

    def test_entities(self, requests_mock):
        requests_mock.get("https://petermaffay.addepar.com/api/v1/entities",
                          json={"data": [{"id": "1", "attributes": {"a": 2.0, "b": 3.0}}], "links": {"next": None}})
        x = {key: attr for key, attr in Request().entities()}
        assert x == {"1": {"a": 2.0, "b": 3.0}}

    def test_entity_id(self, requests_mock):
        requests_mock.get("https://petermaffay.addepar.com/api/v1/entities/1",
                          json={"data": {"id": "1", "attributes": {"a": 2.0, "b": 3.0}}})
        x = Request().entity(id=1)
        assert x == {"a": 2.0, "b": 3.0}

    def test_group_id(self, requests_mock):
        requests_mock.get("https://petermaffay.addepar.com/api/v1/groups/1",
                          json={"data": {"id": "1", "attributes": {"a": 2.0, "b": 3.0}}})
        x = Request().group(id=1)
        assert x == {"a": 2.0, "b": 3.0}

    def test_options(self):
        with patch.object(Request, "entities") as mock:
            Request().options
            mock.assert_called_once_with(link="/v1/entities", modeltype="OPTION")

    def test_persons(self):
        with patch.object(Request, "entities") as mock:
            Request().persons
            mock.assert_called_once_with(link="/v1/entities", modeltype="PERSON_NODE")

    def test_groups(self):
        with patch.object(Request, "entities") as mock:
            Request().groups
            mock.assert_called_once_with(link="/v1/groups")

    def test_users(self):
        with patch.object(Request, "entities") as mock:
            Request().users
            mock.assert_called_once_with(link="/v1/users")

    def test_delete(self):
        with patch("requests.delete") as mock:
            mock.return_value = True
            assert Request().delete(entity="1")

    def test_post(self):
        with patch("requests.post") as mock:
            mock.return_value = AttrDict({"ok": True, "status_code": 200})
            assert Request().post(data=1)

