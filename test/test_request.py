import pytest
from unittest.mock import patch

import pandas as pd
import pandas.util.testing as pdt
from flask import Flask

from pyaddepar.flask_addepar import addepar
from pyaddepar.addeparrequest import AddeparRequest, PortfolioType, AttrDict


@pytest.fixture
def addepar_request():
    # there's no need to expose the entire client...
    app = Flask(__name__)
    # initialize the config of the app object
    app.config.from_pyfile('config/settings.cfg')

    # move into the app context and initialize the amberdata project
    with app.app_context():
        addepar.init_app(app)
        yield addepar.request


def test_version(addepar_request, requests_mock):
    requests_mock.get("https://maffay.addepar.com/api/v1/api_version", json={'a': 'b'})
    y = addepar_request.version
    assert y == {'a': 'b'}


def test_auth(addepar_request):
    assert addepar_request.auth == ("A", "B")


def test_dicturl(addepar_request):
    x = addepar_request.dicturl({"a": 200, "b": "cc"})
    assert x == "a=200&b=cc"


def test_view_csv(addepar_request, requests_mock):
    xxx = pd.DataFrame(index=["x", "y"], columns=["a"], data=[[4], [5]])
    xxx.index.name = "Peter"

    requests_mock.get(
        "https://maffay.addepar.com/api/v1/portfolio/views/10/results?portfolio_id=20&portfolio_type=entity&output_type=csv&start_date=1978-11-12&end_date=1978-11-12",
        text=xxx.to_csv())
    x = addepar_request.view_csv(view_id=10, portfolio_id=20, portfolio_type=PortfolioType.ENTITY,
                           start_date=pd.Timestamp("12-Nov-1978"), end_date=pd.Timestamp("12-Nov-1978"))

    pdt.assert_frame_equal(x, xxx.reset_index())


def test_users(addepar_request,requests_mock):
    requests_mock.get("https://maffay.addepar.com/api/v1/users",
                      json={"data": [{"id": "1", "attributes": {"a": 2.0, "b": 3.0}}], "links": {"next": None}})
    x = {key: attr for key, attr in addepar_request.users}
    assert x == {"1": {"a": 2.0, "b": 3.0}}


def test_user_id(addepar_request,requests_mock):
    requests_mock.get("https://maffay.addepar.com/api/v1/users/1",
                      json={"data": {"id": "1", "attributes": {"a": 2.0, "b": 3.0}}})
    x = addepar_request.user(id=1)
    assert x == {"a": 2.0, "b": 3.0}


def test_entities(addepar_request,requests_mock):
    requests_mock.get("https://maffay.addepar.com/api/v1/entities",
                      json={"data": [{"id": "1", "attributes": {"a": 2.0, "b": 3.0}}], "links": {"next": None}})
    x = {key: attr for key, attr in addepar_request.entities()}
    assert x == {"1": {"a": 2.0, "b": 3.0}}


def test_entity_id(addepar_request,requests_mock):
    requests_mock.get("https://maffay.addepar.com/api/v1/entities/1",
                      json={"data": {"id": "1", "attributes": {"a": 2.0, "b": 3.0}}})
    x = addepar_request.entity(id=1)
    assert x == {"a": 2.0, "b": 3.0}


def test_group_id(addepar_request,requests_mock):
    requests_mock.get("https://maffay.addepar.com/api/v1/groups/1",
                      json={"data": {"id": "1", "attributes": {"a": 2.0, "b": 3.0}}})
    x = addepar_request.group(id=1)
    assert x == {"a": 2.0, "b": 3.0}


def test_options(addepar_request):
    with patch.object(AddeparRequest, "entities") as mock:
        addepar_request.options
        mock.assert_called_once_with(link="/v1/entities", modeltype="OPTION")


def test_persons(addepar_request):
    with patch.object(AddeparRequest, "entities") as mock:
        addepar_request.persons
        mock.assert_called_once_with(link="/v1/entities", modeltype="PERSON_NODE")


def test_groups(addepar_request):
    with patch.object(AddeparRequest, "entities") as mock:
        addepar_request.groups
        mock.assert_called_once_with(link="/v1/groups")


def test_users(addepar_request):
    with patch.object(AddeparRequest, "entities") as mock:
        addepar_request.users
        mock.assert_called_once_with(link="/v1/users")


def test_delete(addepar_request):
    with patch("requests.delete") as mock:
        mock.return_value = True
        assert addepar_request.delete(entity="1")


def test_post(addepar_request):
    with patch("requests.post") as mock:
        mock.return_value = AttrDict({"ok": True, "status_code": 200})
        assert addepar_request.post(data=1)

