# -*- coding: utf-8 -*-
from __future__ import annotations

import pytest
from flask import Flask

from pyaddepar.flask_addepar import Addepar
from pyaddepar.flask_addepar import addepar
from pyaddepar.flask_addepar import InvalidSettingsError


def test_app_false(app):
    # move into the app context and initialize the amberdata project
    with pytest.raises(Exception):
        with app.app_context():
            addepar.init_app(None)


def test_init_addepar(app):
    a = Addepar(app=app)
    assert a


def test_incorrect_config():
    app = Flask(__name__)

    with pytest.raises(InvalidSettingsError):
        a = addepar.init_app(app=app, config=[5.0])
