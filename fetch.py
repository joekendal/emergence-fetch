import json, requests, sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


STOCKS = ['AAPL', 'TSLA', 'AMZN', 'FB', 'IBM', 'SNAP', 'NVDA', 'GOOGL']

# Default returns JSON
URL = "https://financialmodelingprep.com/api/v3/financials/income-statement/"


class Stock(Base):
    __tablename__ = "stocks"
    id = Column(String, primary_key=True) # Ticker Symbol
    financials = relationship("AnnualFinancial", back_populates="stock")

    def __repr__(self):
        return "<Stock(symbol='%s')>" % self.id

class AnnualFinancial(Base):
    __tablename__ = "annualfinancials"
    id = Column(Integer, primary_key=True)
    stock_id = Column(String, ForeignKey('stocks.id'))
    stock = relationship("Stock", back_populates="financials")

    date = Column(Date)
    revenue = Column(Float)
    revenue_growth = Column(Float)
    cost_of_revenue = Column(Float)

    def __repr__(self):
        return "<Financial(stock='%s',date='%s')>" % (self.stock_id, self.date)

def fetch():
    for stock in STOCKS:
        print("fetching %s" % stock)
        r = requests.get(URL+stock)
        if r.status_code == 200:
            session = Session()
            new_stock = Stock(id=stock)
            # Stock may already be in DB but check if all annual financials exist...
            if not session.query(Stock).filter_by(id=stock).one_or_none():
                session.add(new_stock)
                session.commit()
            financials = r.json()['financials']
            # Assumed that financials are ordered most recent at first index
            if not session.query(Stock).filter_by(date=financials[0]['date']).one_or_none():
                for financial in financials:
                    new_financial = AnnualFinancial(
                        stock_id = new_stock.id,
                        date = financial['date'],
                        revenue = financial['Revenue'],
                        revenue_growth = financial['Revenue Growth'],
                        # ...
                    )
                    session.add(new_financial)
                    session.commit()
                    print(new_financial)
        else:
            print("[!] Error fetching %s" % stock)
