#https://lobnek.addepar.com/api/v1/portfolio/views/17949/results?portfolio_id=1&portfolio_type=firm&output_type=csv&start_date=2020-02-11&end_date=2020-03-11&addepar_firm=202


from config.settings import request, pd
from pyaddepar.addeparrequest import PortfolioType

pd.options.display.max_rows = None
pd.options.display.max_columns = None
pd.options.display.width = 500


if __name__ == '__main__':
    x = request.view_csv(view_id=17949, portfolio_id=1, portfolio_type=PortfolioType.FIRM)
    x = x.set_index(keys="Security [Entity ID]").sort_index()

    ticker = x["Lobnek Ticker Symbol Bloomberg"].unique()
    print(ticker)
    print(x)

