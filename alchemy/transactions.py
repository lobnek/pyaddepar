import pandas as pd

from alchemy.aux import session, engine

session = session(engine())

from alchemy.model import Client, Transaction, Account

if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)

    client = session.query(Client).filter(Client.name == "Lafleur 01 UBS").one()
    for account in client.accounts:
        print(account)


    account = client.accounts.filter(Account.name == "EUR 0243-428194.60C PAIEMENTS").one()
    transaction = Transaction(cashflow=200.15,
                              account=account,
                              date=pd.Timestamp("today").date(),
                              comment="My first transaction")

    session.add(transaction)
    session.commit()

    for transaction in session.query(Transaction).all():
        print(transaction)
        print(transaction.date)
        print(transaction.account)
        print(transaction.account.client)
        print(transaction.account.client.adp_entity)
        print(transaction.account.client.name)
        print(transaction.comment)


    assert False

    for client in session.query(Client).all():
        print(client.name)
        for account in client.accounts:
            print(account)
        print("*" * 100)

