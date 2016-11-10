import pandas as pd
from sqlalchemy.exc import IntegrityError

pd.set_option("display.width", 300)

x = pd.read_csv("master.csv", index_col=0)

from alchemy.aux import session, engine
session = session(engine())


def add(object):
    try:
        session.add(object)
        session.commit()
    except IntegrityError:
        session.rollback()


from alchemy.model import Cash, Security

if __name__ == '__main__':
    print(x.keys())
    for name, row in x.iterrows():
        cash = session.query(Cash).filter(Cash.name==row["Currency"]).one()
        security = Security(name=name,  cash=cash, isin=row["ISIN"], ticker=row["Ticker Symbol"], adp_entity=row["Entity ID"])
        add(security)
