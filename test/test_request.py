from unittest import TestCase

import requests_mock

from pyaddepar.request import Request


class TestRequest(TestCase):
    def test_version(self):
        with requests_mock.mock() as m:
            r = Request(key=1, secret=1, id="maffay", company="maffay")
            m.get("https://maffay.addepar.com/api/v1/api_version", json={'a':'b'})
            y = r.version
            self.assertEqual(y.json(), {'a':'b'})
