import json, requests, sqlalchemy, datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


STOCKS = ['AAPL', 'TSLA', 'AMZN', 'FB', 'IBM', 'SNAP', 'NVDA', 'GOOGL']

# Default returns JSON
ANNUAL_INCOME_STATEMENT_URL = "https://financialmodelingprep.com/api/v3/financials/income-statement/"


class Stock(Base):
    __tablename__ = "stocks"
    id = Column(String, primary_key=True) # Ticker Symbol
    income_statements = relationship("AnnualIncomeStatement", back_populates="stock")

    def __repr__(self):
        return "<Stock(symbol='%s')>" % self.id

class AnnualIncomeStatement(Base):
    __tablename__ = "annualincomestatements"

    # Composite key
    stock_id = Column(String, ForeignKey('stocks.id'), primary_key=True)
    date = Column(Date, primary_key=True)

    stock = relationship("Stock", back_populates="income_statements")

    revenue = Column(Float)
    revenue_growth = Column(Float)
    cost_of_revenue = Column(Float)
    gross_profit = Column(Float)
    r_and_d_expenses = Column(Float)
    sg_and_a_expense = Column(Float)
    operating_expenses = Column(Float)
    operating_income = Column(Float)
    interest_expense = Column(Float)
    earnings_pre_tax = Column(Float)
    income_tax_expense = Column(Float)
    net_income_non_controlling = Column(Float)
    net_income_discontinued_ops = Column(Float)
    net_income = Column(Float)
    preferred_dividends = Column(Float)
    net_income_com = Column(Float)
    eps = Column(Float)
    eps_diluted = Column(Float)
    weighted_avg_shs_out = Column(Float)
    weighted_avg_shs_out_dil = Column(Float)
    dividend_per_share = Column(Float)
    gross_margin = Column(Float)
    ebitda_margin = Column(Float)
    ebit_margin = Column(Float)
    profit_margin = Column(Float)
    free_cash_flow_margin = Column(Float)
    ebitda = Column(Float)
    ebit = Column(Float)
    consolidated_income = Column(Float)
    earnings_pre_tax_margin = Column(Float)
    net_profit_margin = Column(Float)

    def __repr__(self):
        return "<IncomeStatement(stock='%s',date='%s')>" % (self.stock_id, self.date)

def fetch():
    session = Session()
    for stock in STOCKS:
        print("[*] Fetching %s..." % stock)
        r = requests.get(ANNUAL_INCOME_STATEMENT_URL+stock)
        if r.status_code == 200:
            if not session.query(Stock).filter_by(id=stock).one_or_none():
                new_stock = Stock(id=stock)
                session.add(new_stock)
                session.commit()

            income_statements = r.json()['financials']

            for statement in income_statements:
                statement_date = datetime.datetime.strptime(statement['date'], '%Y-%m-%d').date()
                if not session.query(AnnualIncomeStatement)\
                    .filter(AnnualIncomeStatement.stock_id==stock,
                            AnnualIncomeStatement.date==statement_date).one_or_none():
                    new_statement = AnnualIncomeStatement(
                        stock_id = stock,
                        date = statement_date,
                        revenue = statement['Revenue'],
                        revenue_growth = statement['Revenue Growth'] or None,
                        cost_of_revenue = statement['Cost of Revenue'],
                        gross_profit = statement['Gross Profit'],
                        r_and_d_expenses = statement['R&D Expenses'],
                        sg_and_a_expense = statement['SG&A Expense'],
                        operating_expenses = statement['Operating Expenses'],
                        operating_income = statement['Operating Income'],
                        interest_expense = statement['Interest Expense'],
                        earnings_pre_tax = statement['Earnings before Tax'],
                        income_tax_expense = statement['Income Tax Expense'],
                        net_income_non_controlling = statement['Net Income - Non-Controlling int'],
                        net_income_discontinued_ops = statement['Net Income - Discontinued ops'],
                        net_income = statement['Net Income'],
                        preferred_dividends = statement['Preferred Dividends'],
                        net_income_com = statement['Net Income Com'],
                        eps = statement['EPS'],
                        eps_diluted = statement['EPS Diluted'],
                        weighted_avg_shs_out = statement['Weighted Average Shs Out'] or None,
                        weighted_avg_shs_out_dil = statement['Weighted Average Shs Out (Dil)'] or None,
                        dividend_per_share = statement['Dividend per Share'],
                        gross_margin = statement['Gross Margin'],
                        ebitda_margin = statement['EBITDA Margin'],
                        ebit_margin = statement['EBIT Margin'],
                        profit_margin = statement['Profit Margin'],
                        free_cash_flow_margin = statement['Free Cash Flow margin'],
                        ebitda = statement['EBITDA'],
                        ebit = statement['EBIT'],
                        consolidated_income = statement['Consolidated Income'],
                        earnings_pre_tax_margin = statement['Earnings Before Tax Margin'],
                        net_profit_margin = statement['Net Profit Margin']
                    )
                    session.add(new_statement)
                    session.commit()
        else:
            print("[!] Error fetching %s" % stock)


"""
To find financials for stock by year

session.query(AnnualIncomeStatement).join(Stock)\
        .filter(Stock.id=='AAPL')\
        .filter(AnnualIncomeStatement.date.like("2018%"))\
        .one_or_none()
or...

session.query(AnnualIncomeStatement)\
    .filter(AnnualIncomeStatement.stock_id=='AAPL', AnnualIncomeStatement.date.like("2018%"))\
    .one_or_none()

"""
