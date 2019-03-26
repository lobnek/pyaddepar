from pyaddepar.request import Request

if __name__ == '__main__':
    r = Request()

    x = {
        "data": {
        "type": "entities",
        "attributes": {
            "original_name": "Thomas Schmelzer",
            "currency_factor": "CHF",
            "model_type": "PERSON_NODE"
        }
    }
    }

    r.post(x)
    #for x in [5504500, 5504501, 5504502]:
    #    r.delete(x)
