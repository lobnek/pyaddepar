import pytest
from flask import Flask

from pyaddepar.flask_addepar import addepar, InvalidSettingsError, Addepar


def test_app_false():
    app = Flask(__name__)
    # initialize the config of the app object
    app.config.from_pyfile('/addepar/test/config/settings.cfg')

    # move into the app context and initialize the amberdata project
    with pytest.raises(Exception):
        with app.app_context():
            addepar.init_app(None)


def test_init_addepar():
    app = Flask(__name__)
    # initialize the config of the app object
    app.config.from_pyfile('/addepar/test/config/settings.cfg')

    a = Addepar(app=app)
    assert a


def test_incorrect_config():
    app = Flask(__name__)
    # initialize the config of the app object
    # app.config.from_pyfile('/amberdata/test/config/settings.cfg')

    with pytest.raises(InvalidSettingsError):
        a = addepar.init_app(app=app, config=[5.0])


def test_initapp_double():
    app = Flask(__name__)
    # initialize the config of the app object
    app.config.from_pyfile('config/settings.cfg')

    a = Addepar(app=app)

    with pytest.raises(Exception):
        a.init_app(app=app)
