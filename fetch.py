import json, requests, sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()



STOCKS = ['AAPL', 'TSLA', 'AMZN', 'FB', 'IBM', 'SNAP', 'NVDA', 'GOOGL']

# Default returns JSON
QUARTERLY_URL = "https://financialmodelingprep.com/api/v3/financials/income-statement/"


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(String, primary_key=True) # Ticker Symbol

    def __repr__(self):
        return "<Stock(symbol='%s')>" % self.id

class Financials:

    id = Column(Integer, primary_key=True)
    date = Column()


for stock in STOCKS:
    print("fetching %s" % stock)
    r = requests.get(QUARTERLY_URL+stock)
    print(r.status_code)

    input()
