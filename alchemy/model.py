from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Float, Date, Text


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    adp_entity = Column(String, unique=True)
    accounts = relationship("Account", lazy='dynamic')

    def __repr__(self):
        return "<Client(name={0})>".format(self.name)


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    # Note that the Addepar entity code does not have to be unique for an account. Cash account problem!
    adp_entity = Column(String)
    name = Column(String)
    client_id = Column(Integer, ForeignKey("client.id"))
    cash_id = Column(Integer, ForeignKey("cash.id"))

    client = relationship("Client", back_populates="accounts")
    cash = relationship("Cash", back_populates="accounts")

    __table_args__ = (UniqueConstraint('adp_entity', 'name', 'cash_id', 'client_id'),)

    transactions = relationship("Transaction", lazy='dynamic')

    def __repr__(self):
        return "<Account(name={0}, cash={1})>".format(self.name, self.cash)


class Cash(Base):
    __tablename__ = 'cash'

    id = Column(Integer, primary_key=True)
    adp_entity = Column(String, unique=True)
    name = Column(String, unique=True)
    accounts = relationship("Account", lazy='dynamic')
    securities = relationship("Security", lazy='dynamic')

    def __repr__(self):
        return "<Cash(name={0})>".format(self.name)


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    account = relationship("Account", back_populates="transactions")
    cashflow = Column(Float)
    date = Column(Date)
    comment = Column(Text)

    def __repr__(self):
        return "<Transactions(Account={0}, cashflow={1})>".format(self.account, self.cashflow)


class Security(Base):
    __tablename__ = 'security'
    id = Column(Integer, primary_key=True)
    adp_entity = Column(String, unique=True)
    cash_id = Column(Integer, ForeignKey("cash.id"))
    cash = relationship("Cash", back_populates="securities")
    isin = Column(String, nullable=True)
    ticker = Column(String, nullable=True)
    name = Column(String, unique=True)


if __name__ == '__main__':
    from alchemy.aux import engine
    Base.metadata.create_all(engine(echo=True))
