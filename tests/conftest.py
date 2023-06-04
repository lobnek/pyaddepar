# -*- coding: utf-8 -*-
"""global fixtures"""
from __future__ import annotations

from pathlib import Path

import pytest
from flask import Flask


@pytest.fixture(scope="session", name="resource_dir")
def resource_fixture():
    """resource fixture"""
    return Path(__file__).parent / "resources"


@pytest.fixture()
def app(resource_dir):
    app = Flask(__name__)
    # initialize the config of the app object
    app.config.from_pyfile(resource_dir / "config" / "settings.cfg")
    return app
