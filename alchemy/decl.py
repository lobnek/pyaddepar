from alchemy.cash import cash_series
from pyaddepar.preader import PReader
from auth import aFirm, aKey, aSecret
from sqlalchemy.exc import IntegrityError
from alchemy.aux import session, engine

session = session(engine())

from alchemy.model import Cash, Client, Account


def add(object):
    try:
        session.add(object)
        session.commit()
    except IntegrityError:
        session.rollback()


if __name__ == '__main__':
    # all the cash
    for cash in cash_series():
        add(cash)

    cash_ids = [cash.adp_entity for cash in session.query(Cash).all()]

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = PReader(id=aFirm, key=aKey, secret=aSecret)

    # get all the addepar entities
    ent = reader.entities

    print(ent)
    assert False

    for group_id, group in reader.groups.items():
        for adp_entity, name in group.owns.items():
            # only interested in real clients
            if int(adp_entity) < 1e6:
                add(Client(adp_entity=adp_entity, name=name))

    for client in session.query(Client).all():
        edges = reader.positions().edges([client.adp_entity])

        cond1 = (edges.index.get_level_values('Owner ID') == client.adp_entity)
        cond2 = (edges.index.get_level_values('Owned ID').isin(cash_ids))

        edges = edges.ix[cond1 | cond2].reset_index(level=0)
        for entity_id, edge in edges.iterrows():
            cash = session.query(Cash).filter(Cash.name == ent.ix[entity_id]["Currency"]).one()
            account = Account(adp_entity=entity_id, cash=cash, client=client, name=edge["Position Name"])
            add(account)
