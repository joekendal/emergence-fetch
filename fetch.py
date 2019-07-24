import json, requests
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import *


engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)


STOCKS = ['AAPL', 'TSLA', 'AMZN', 'FB', 'IBM', 'SNAP', 'NVDA', 'GOOGL']

def get_financial_statements(stock, db):

    statement_types = [
        {
            "URL": "https://financialmodelingprep.com/api/v3/financials/income-statement/",
            "Model": AnnualIncomeStatement
        },
        {
            "URL": "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/",
            "Model": AnnualBalanceSheet
        },
        {
            "URL": "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/",
            "Model": AnnualCashFlow
        }
    ]

    for statement_type in statement_types:

        r = requests.get(statement_type['URL']+stock)
        if r.status_code == 200:
            if not db.query(Stock).filter_by(id=stock).one_or_none():
                new_stock = Stock(id=stock)
                db.add(new_stock)
                db.commit()

            statements = r.json()['financials']

            for statement in statements:
                statement_date = datetime.strptime(statement['date'], '%Y-%m-%d').date()
                if not db.query(statement_type['Model'])\
                    .filter(statement_type['Model'].stock_id==stock,
                            statement_type['Model'].date==statement_date).one_or_none():

                    if statement_type['Model'] == AnnualIncomeStatement:
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
                    elif statement_type['Model'] == AnnualBalanceSheet:
                        new_statement = AnnualBalanceSheet(
                            stock_id = stock,
                            date = statement_date,
                            cash_and_equiv = statement['Cash and cash equivalents'],
                            short_term_investments = statement['Short-term investments'],
                            cash_and_short_term_investments = statement['Cash and short-term investments'],
                            receivables = statement['Receivables'],
                            inventories = statement['Inventories'],
                            total_current_assets = statement['Total current assets'],
                            property_plant_and_equipment_net = statement['Property, Plant & Equipment Net'],
                            goodwill_and_intangible_assets = statement['Goodwill and Intangible Assets'],
                            long_term_investments = statement['Long-term investments'],
                            tax_assets = statement['Tax assets'],
                            total_non_current_assets = statement['Total non-current assets'],
                            total_assets = statement['Total assets'],
                            payables = statement['Payables'],
                            short_term_debt = statement['Short-term debt'],
                            total_current_liabilities = statement['Total current liabilities'],
                            long_term_debt = statement['Long-term debt'],
                            total_debt = statement['Total debt'],
                            deferred_revenue = statement['Deferred revenue'],
                            tax_liabilities = statement['Tax Liabilities'],
                            deposit_liabilities = statement['Deposit Liabilities'],
                            total_non_current_liabilities = statement['Total non-current liabilities'],
                            total_liabilities = statement['Total liabilities'],
                            other_comprehensive_income = statement['Other comprehensive income'],
                            retained_earnings_deficit = statement['Retained earnings (deficit)'],
                            total_shareholders_equity = statement['Total shareholders equity'],
                            investments = statement['Investments'],
                            net_debt = statement['Net Debt'],
                            other_assets = statement['Other Assets'],
                            other_liabilities = statement['Other Liabilities']
                        )

                    elif statement_type['Model'] == AnnualCashFlow:
                        new_statement = AnnualCashFlow(
                            stock_id = stock,
                            date = statement_date,
                            depreciation_and_amortization = statement['Depreciation & Amortization'],
                            stock_based_compensation = statement['Stock-based compensation'],
                            operating_cash_flow = statement['Operating Cash Flow'],
                            capital_expenditure = statement['Capital Expenditure'],
                            acquisitions_and_disposals = statement['Acquisitions and disposals'],
                            investment_purchases_and_sales = statement['Investment purchases and sales'],
                            investing_cash_flow = statement['Investing Cash flow'],
                            issuance_repayment_of_debt = statement['Issuance (repayment) of debt'],
                            issuance_buybacks_of_shares = statement['Issuance (buybacks) of shares'],
                            dividend_payments = statement['Dividend payments'],
                            financing_cash_flow = statement['Financing Cash Flow'],
                            effect_of_forex_changes_on_cash = statement['Effect of forex changes on cash'],
                            net_cash_flow = statement['Net cash flow / Change in cash'],
                            free_cash_flow = statement['Free Cash Flow'],
                            net_cash = statement['Net Cash/Marketcap']
                        )

                    db.add(new_statement)
                    db.commit()
        else:
            print("[!] Error fetching %s Income Statements" % stock)



def fetch():
    db = Session()
    for stock in STOCKS:
        print("[*] Fetching %s..." % stock)
        get_financial_statements(stock, db)

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
