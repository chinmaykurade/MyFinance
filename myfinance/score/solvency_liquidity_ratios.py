import pandas as pd

def solvency_liquidity_ratios(company_table, company_info, company_name="Name", replace=False):
    company_table = company_table.fillna(0)

    # Drop duplicate columns
    # company_table = company_table.loc[:, ~company_table.columns.duplicated()]

    # Check if EBITDA is not in the table (generally finance stocks, excluded for now)
    if 'EBITDA' not in list(company_table.columns):
        print("Excluded: ", company_name)
        return None

    if 'Inventory' not in list(company_table.columns):
        company_table['Inventory'] = 0

    if replace:
        new_table = pd.DataFrame(columns=company_table.columns, index=company_table.index)
    else:
        new_table = company_table.copy()

    new_table['EBIT'] = company_table['EBITDA'] - company_table['Depreciation & amortisation']

    if 'Long-term debt' not in list(company_table.columns):
        company_table['Long-term debt'] = 0

    if 'Current debt' not in list(company_table.columns):
        company_table['Current debt'] = 0

    new_table['DE'] = 2 * company_table['Long-term debt'] / \
                           (company_table["Total stockholders' equity"] +
                            company_table["Total stockholders' equity"].shift(-1))

    new_table['Interest Coverage Ratio'] = new_table['EBIT'] / company_table['Interest expense']

    new_table['Equity Multiplier'] = (company_table['Total assets'] + company_table["Total assets"].shift(-1))/\
                           (company_table["Total stockholders' equity"] +
                            company_table["Total stockholders' equity"].shift(-1))

    # Liquidity Ratios
    new_table['Current Ratio'] = company_table['Total current assets'] / company_table['Total current liabilities']

    new_table['Quick Ratio'] = (company_table['Total current assets'] - company_table['Inventory'])/ \
                                   company_table['Total current liabilities']

    new_table['Cash Ratio'] = company_table['Total cash'] / company_table['Total current liabilities']

    return new_table
