from sqlalchemy import create_engine


def engine(connection_string=None, echo=False):
    connection_string = connection_string or 'postgresql://postgres:excalibur@dbsrv:5432/addepar'
    return create_engine(connection_string, echo=echo)


def session(engine):
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    return Session()
