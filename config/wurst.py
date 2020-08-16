from config.settings import request, pd
from pyaddepar.addeparrequest import PortfolioType

pd.options.display.max_rows = None
pd.options.display.max_columns = None
pd.options.display.width = 500


class Portfolio(object):
    def __init__(self, id, start=None):
        self.__id = id
        start = start or pd.Timestamp("2010-01-01")
        self.__transaction = request.transaction_csv(view_id=1974, portfolio_id=self.id,
                                                     portfolio_type=PortfolioType.ENTITY, start_date=start)
        self.__transaction = self.__transaction.set_index(
            keys=["Posted Date", "Trade Date", "Settle Date"]).sort_index()

        self.__latest = request.view_csv(view_id=52968, portfolio_id=self.id, portfolio_type=PortfolioType.ENTITY)
        self.__latest = self.__latest.set_index(keys=["Security"]).sort_index()


    @property
    def id(self):
        return self.__id

    @property
    def transaction(self):
        return self.__transaction

    @property
    def init_cash(self):
        x = self.transaction
        cash = x[x["Type"] == "Transfer In"]
        assert cash["Security"].values[0] == "USD Cash"
        return cash["Value"].values[0]

    def filter(self, take=None, out=None):
        if out is not None:
            return self.transaction[~(self.transaction.Type.isin(out))]

        if take is not None:
            return self.transaction[self.transaction.Type.isin(take)]

    @property
    def securities(self):
        for name, group in self.filter(out={"Transfer In", "Open Position", "Account Fee (Custodian)", "Account Fee (Management)"}).groupby(by="Security"):
            ids = group["Security [Entity ID]"].unique()
            assert len(ids) == 1
            yield name, ids[0]

    @property
    def __values(self):
        for name, group in self.filter(take={"Buy", "Sell", "Corporate Action"}).groupby(by="Security"):
            # what happens if multiple transactions for the same security have the same settle date ==> sum
            v = group["Value"].groupby("Settle Date").sum()
            yield name, v

    @property
    def __units(self):
        for name, group in self.filter(take={"Buy", "Sell", "Corporate Action"}).groupby(by="Security"):
            # what happens if multiple transactions for the same security have the same settle date ==> sum
            d = group["Units"].groupby("Settle Date").sum().cumsum()
            yield name, d

    @property
    def __dividend(self):
        for name, group in self.filter(take={"Dividend (Of Cash)"}).groupby(by="Security"):
            # what happens if multiple transactions for the same security have the same settle date ==> sum
            yield name, (group["Value"].groupby("Settle Date").sum())

    @property
    def fee(self):
        return self.filter(take={"Account Fee (Management)", "Account Fee (Custodian)"})["Value"].groupby("Settle Date").sum()

    @property
    def bloomberg(self):
        entities = {name: data for name, data in request.entities()}

        for name, entity in p.securities:
            data = entities[str(entity)]
            yield name, data['_custom_bloomberg_ticker_symbol_lwm_141101'][0]["value"]

    @property
    def position(self):
        return pd.DataFrame({asset: unit for asset, unit in p.__units}).ffill().fillna(0.0)

    @property
    def values(self):
        return pd.DataFrame({asset: value for asset, value in p.__values}).fillna(0.0)

    @property
    def dividend(self):
        return pd.DataFrame({asset: value for asset, value in p.__dividend}).fillna(0.0)

    @property
    def latest(self):
        return self.__latest

p = Portfolio(id=1025957)

d = dict()
d["Transactions"] = p.values.sum(axis=1).cumsum()
d["Dividends"] = p.dividend.sum(axis=1).cumsum()
d["Transfer In"] = p.init_cash
d["Fees"] = p.fee.cumsum()

x = pd.DataFrame(d).ffill()
x = x.sum(axis=1)
print(x.tail(5))


#https://lobnek.addepar.com/api/v1/portfolio/views/119879/results?portfolio_id=1025957&portfolio_type=entity&output_type=csv&start_date=2020-02-10&end_date=2020-03-10&addepar_firm=202

# Bloomberg Tickers...
#https://lobnek.addepar.com/api/v1/portfolio/views/119879/results?portfolio_id=1&portfolio_type=firm&output_type=csv&start_date=2020-02-10&end_date=2020-03-10&addepar_firm=202

#https://lobnek.addepar.com/api/v1/portfolio/views/17949/results?portfolio_id=1025957&portfolio_type=entity&output_type=csv&start_date=2020-02-10&end_date=2020-03-10&addepar_firm=202
