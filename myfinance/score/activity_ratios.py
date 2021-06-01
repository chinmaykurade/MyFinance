import pandas as pd

def activity_ratios(company_table, company_info, company_name="Name", replace=False):
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

    new_table['Total Asset Turnover'] = 2 * company_table['Total revenue'] / \
                            (company_table['Total assets'] + company_table['Total assets'].shift(-1))

    new_table['Fixed Asset Turnover'] = 2 * company_table['Total revenue'] / \
                                            (company_table['Total non-current assets'] +
                                             company_table['Total non-current assets'].shift(-1))

    try:
        new_table['Working Capital'] = company_table['Net receivables'] + company_table['Inventory'] - \
                                           company_table['Accounts payable']
    except:
        print("Inventory ", company_name)
        return None

    new_table['Working Capital Turnover'] = 2 * company_table['Total revenue'] / \
                                            (new_table['Working Capital'] +
                                             new_table['Working Capital'].shift(-1))

    new_table['Receivables Turnover'] = 2 * company_table['Total revenue'] / \
                                            (company_table['Net receivables'] +
                                             company_table['Net receivables'].shift(-1))

    # (No. of days required to recover sales cash from customers)
    new_table['Days Receivables Outstanding'] = 365/new_table['Receivables Turnover']

    new_table['Inventory Turnover'] = 2 * company_table['Cost of revenue'] / \
                                            (company_table['Inventory'] +
                                             company_table['Inventory'].shift(-1))

    new_table['Days Inventory Held'] = 365/new_table['Inventory Turnover']

    new_table['Purchases'] = company_table['Inventory'] - company_table['Inventory'].shift(-1) \
                                 + company_table['Cost of revenue']

    new_table['Payables Turnover'] = 2 * new_table['Purchases'] / \
                                            (company_table['Accounts payable'] +
                                             company_table['Accounts payable'].shift(-1))

    new_table['Days Payables Outstanding'] = 365/new_table['Payables Turnover']

    # Cash Conversion Cycle = Days Receivables Outstanding + Days Inventory Held – Days Payables Outstanding
    new_table['Cash Conversion Cycle'] = new_table['Days Receivables Outstanding'] + \
                                             new_table['Days Inventory Held'] -\
                                             new_table['Days Payables Outstanding']

    return new_table