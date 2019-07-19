import json, requests, sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()



STOCKS = ['AAPL', 'TSLA', 'AMZN', 'FB', 'IBM', 'SNAP', 'NVDA', 'GOOGL']

# Default returns JSON
URL = "https://financialmodelingprep.com/api/v3/financials/income-statement/"


class Stock(Base):
    __tablename__ = "stocks"
    id = Column(String, primary_key=True) # Ticker Symbol

    def __repr__(self):
        return "<Stock(symbol='%s')>" % self.id

class AnnualFinancial(Base):
    __tablename__ = "annualfinancials"
    id = Column(Integer, primary_key=True)
    stock_id = Column(String, ForeignKey('stocks.id'))

    date = Column(Date)
    revenue = Column(Float)
    revenue_growth = Column(Float)
    cost_of_revenue = Column(Float)

    def __repr__(self):
        return "<Financial(stock='%s',date='%s')>" % (self.stock_id, self.date)


for stock in STOCKS:
    print("fetching %s" % stock)
    r = requests.get(URL+stock)
    if r.status_code == 200:
        new_stock = Stock(
            id = stock,
        )
        financials = r.json()['financials']
        for financial in financials:
            new_financial = AnnualFinancial(
                stock_id = new_stock.id,
                date = financial['date'],
                revenue = financial['Revenue'],
                revenue_growth = financial['Revenue Growth']
            )
            print(new_financial)
