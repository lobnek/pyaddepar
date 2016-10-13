from alchemy.model import Cash


def cash_series():
    cash = {"GBP": "856263", "USD": "804348", "EUR": "827363", "CHF": "856262",
            "MXN": "840308", "SGD": "867344", "JPY": "827364", "CAD": "840360",
            "HKD": "827365"}

    return [Cash(name=name, adp_entity=adp) for name, adp in cash.items()]

if __name__ == '__main__':
    print(cash_series())