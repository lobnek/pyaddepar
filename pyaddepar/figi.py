import json

from requests import post


def figi(idValue, idType, openfigi_apikey):
    """
    :param idValue: The value of the identifier, e.g. "CARSECC"
    :param idType: The type of the identifier, e.g. "TICKER". See https://www.openfigi.com/api for a list of choices
    :param openfigi_apikey: Sign up at https://www.openfigi.com/user/signup to get your own openfigi_apikey

    :return: a dictionary with plenty of meta data for the requested symbol
    """
    header = {'Content-type': 'application/json', 'X-OPENFIGI-APIKEY': openfigi_apikey}
    url = 'https://api.openfigi.com/v1/mapping'
    x = post(url=url, headers=header, data=json.dumps([{"idType": idType, "idValue": idValue}]))
    return x.json()[0]["data"][0]