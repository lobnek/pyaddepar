import pandas as pd

from alchemy.aux import session, engine
session = session(engine())

from alchemy.model import Client


if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)

    for client in session.query(Client).all():
        print(client.name)
        for account in client.accounts:
            print(account)
        print("*"*100)
