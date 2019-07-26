from sqlalchemy import create_engine, Column, Float, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Stock(Base):
    __tablename__ = "stocks"
    symbol = Column(String, primary_key=True) # Ticker Symbol
    name = Column(String)

    income_statements = relationship("AnnualIncomeStatement", back_populates="stock", cascade='all, delete-orphan')
    balance_sheets = relationship("AnnualBalanceSheet", back_populates="stock", cascade='all, delete-orphan')
    cash_flows = relationship("AnnualCashFlow", back_populates="stock", cascade='all, delete-orphan')
    historical_prices = relationship("HistoricalPrice", back_populates="stock", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Stock(symbol='%s',name='%s')>" % (self.symbol, self.name)


class HistoricalPrice(Base):
    __tablename__ = "historicalprices"
    stock_id = Column(String, ForeignKey('stocks.symbol'), primary_key=True)
    date = Column(Date, primary_key=True)

    stock = relationship("Stock", back_populates="historical_prices")

    close = Column(Float, nullable=False)

    def __repr__(self):
        return "<HistoricalPrice(symbol='%s',date='%s',close='%s')>" % (self.stock_id, self.date, self.close)


class AnnualIncomeStatement(Base):
    __tablename__ = "annualincomestatements"

    stock_id = Column(String, ForeignKey('stocks.symbol'), primary_key=True)
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


class AnnualBalanceSheet(Base):
    __tablename__ = "annualbalancesheets"

    stock_id = Column(String, ForeignKey('stocks.symbol'), primary_key=True)
    date = Column(Date, primary_key=True)

    stock = relationship("Stock", back_populates="balance_sheets")

    cash_and_equiv = Column(Float)
    short_term_investments = Column(Float)
    cash_and_short_term_investments = Column(Float)
    receivables = Column(Float)
    inventories = Column(Float)
    total_current_assets = Column(Float)
    property_plant_and_equipment_net = Column(Float)
    goodwill_and_intangible_assets = Column(Float)
    long_term_investments = Column(Float)
    tax_assets = Column(Float)
    total_non_current_assets = Column(Float)
    total_assets = Column(Float)
    payables = Column(Float)
    short_term_debt = Column(Float)
    total_current_liabilities = Column(Float)
    long_term_debt = Column(Float)
    total_debt = Column(Float)
    deferred_revenue = Column(Float)
    tax_liabilities = Column(Float)
    deposit_liabilities = Column(Float)
    total_non_current_liabilities = Column(Float)
    total_liabilities = Column(Float)
    other_comprehensive_income = Column(Float)
    retained_earnings_deficit = Column(Float)
    total_shareholders_equity = Column(Float)
    investments = Column(Float)
    net_debt = Column(Float)
    other_assets = Column(Float)
    other_liabilities = Column(Float)

    def __repr__(self):
        return "<BalanceSheet(stock='%s',date='%s')>" % (self.stock_id, self.date)


class AnnualCashFlow(Base):
    __tablename__ = "annualcashflows"

    stock_id = Column(String, ForeignKey('stocks.symbol'), primary_key=True)
    date = Column(Date, primary_key=True)

    stock = relationship("Stock", back_populates="cash_flows")

    depreciation_and_amortization = Column(Float)
    stock_based_compensation = Column(Float)
    operating_cash_flow = Column(Float)
    capital_expenditure = Column(Float)
    acquisitions_and_disposals = Column(Float)
    investment_purchases_and_sales = Column(Float)
    investing_cash_flow = Column(Float)
    issuance_repayment_of_debt = Column(Float)
    issuance_buybacks_of_shares = Column(Float)
    dividend_payments = Column(Float)
    financing_cash_flow = Column(Float)
    effect_of_forex_changes_on_cash = Column(Float)
    net_cash_flow = Column(Float)
    free_cash_flow = Column(Float)
    net_cash = Column(Float)

    def __repr__(self):
        return "<CashFlow(stock='%s',date='%s')>" % (self.stock_id, self.date)


class c:
    """
    Terminal output colours
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
