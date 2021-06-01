import pandas as pd

def profitability_ratios(company_table, company_info, company_name='Name', replace=False):
    company_table = company_table.fillna(0)

    # Drop duplicate columns
    # company_table = company_table.loc[:, ~company_table.columns.duplicated()]

    # Check if EBITDA is not in the table (generally finance stocks, excluded for now)
    if 'EBITDA' not in list(company_table.columns):
        print("Excluded: ", company_name)
        return None

    if replace:
        new_table = pd.DataFrame(columns=company_table.columns, index=company_table.index)
    else:
        new_table = company_table.copy()

    new_table['EBIT'] = company_table['EBITDA'] - company_table['Depreciation & amortisation']
    new_table['NOPAT'] = new_table['EBIT'] - company_table['Income tax expense']

    if 'Long-term debt' not in list(company_table.columns):
        company_table['Long-term debt'] = 0

    if 'Current debt' not in list(company_table.columns):
        company_table['Current debt'] = 0

    # Enterprise value = Market cap + Debt - Cash
    new_table['EV'] = company_info['market_cap'] + company_table['Long-term debt'] + \
                          company_table['Current debt'] - company_table['Total cash']

    new_table['Earnings Yield'] = new_table['EBIT'] / new_table['EV']

    # Invested Capital = fixed assets + intangible assets + current assets – current liabilities – cash
    new_table['Invested Capital'] = company_table['Total non-current assets'] + \
                                        company_table['Total current assets'] - company_table['Total cash'] \
                                        - company_table['Total current liabilities']

    # Capital employed = shareholders’ equity + long-term debt liabilities
    # 			       = total assets – current liabilities
    new_table['Capital Employed'] = company_table['Total assets'] - company_table['Total current liabilities']

    # ROCE= Earnings Before Interest And Tax(EBIT) ÷ Capital Employed
    new_table['ROCE'] = 2 * new_table['EBIT'] /\
                            (new_table['Capital Employed'] + new_table['Capital Employed'].shift(-1))

    # ROIC = Net Profit After Tax ÷ Invested Capital
    new_table['ROIC'] = 2 * new_table['NOPAT'] / \
                            (new_table['Invested Capital'] + new_table['Invested Capital'].shift(-1))

    # ROA = Net Income / Average(Total Assets)
    new_table['ROA'] = 2 * company_table['Net income'] / \
                            (company_table['Total assets'] + company_table['Total assets'].shift(-1))

    # ROE = Net Income / Average(Total Shareholders Equity)
    new_table['ROE'] = 2 * company_table['Net income'] / \
                           (company_table["Total stockholders' equity"] + company_table[
                               "Total stockholders' equity"].shift(-1))

    # Gross profit margin
    new_table['GPM'] = company_table['EBITDA'] / company_table['Total revenue']

    # Operating profit margin
    new_table['OPM'] = new_table['EBIT'] / company_table['Total revenue']

    # Net profit margin
    new_table['NPM'] = company_table['Net income'] / company_table['Total revenue']

    return new_table
