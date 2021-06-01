# %% Constants definition
points_de = [0.1, 0.2, 0.5, 0.8, 1, 1.5, 2, 2.5, 3, 4]
points_roe = [0, 1, 2, 4, 7, 10, 13, 17, 21, 27]
points_pe = [8, 12, 20, 30, 40, 50, 60, 70, 80, 100]
points_rev = [0, 1, 2.5, 5, 7.5, 10, 12.5, 15, 20, 30]
points_pat = points_rev
weights = [0, 2, 3, 4, 4]


# %% Functions and class definition
def get_score(points, value, minM=True):
    if value is None:
        return 0
    i = 0
    while value > points[i]:
        i += 1
        if i == 10:
            break
    if i != 10:
        factor = (value - points[i - 1]) / (points[i] - points[i - 1])
    else:
        factor = 1
    if minM:
        i = 10 - i
        if i == 10:
            return i
        return i - factor
    else:
        if i == 0:
            return i
        return i + factor - 1


def get_basic_score(values):
    de = get_score(points_de, values['D/E'], minM=True)
    pe = get_score(points_pe, values['P/E'], minM=True)
    roe = get_score(points_roe, values['ROE'], minM=False)
    rev = get_score(points_rev, values['Revenue Growth'], minM=False)
    pat = get_score(points_pat, values['PAT Growth'], minM=False)

    ratio_score = 5 * roe + 3 * de + 2 * pe
    ratio_score /= 10

    sc = rev * 0.3 + pat * 0.5 + ratio_score * 0.2

    return sc


def get_ratios(company_table, company_info):
    # Get the D/E ratio
    borrowings = company_table['Current debt'].iloc[0] + company_table['Long-term debt'].iloc[0]
    reserves = company_table['Retained earnings'].iloc[0]
    share_capital = company_table["Total stockholders' equity"].iloc[0]
    de = borrowings / (share_capital + reserves)

    # Current and quick ratio
    current_ratio = company_table['Current Ratio'].iloc[0]
    quick_ratio = company_table['Quick Ratio'].iloc[0]

    # Drop the September columns
    # sep_rows = [row for row in company_table.index if row.lower().startswith('sep')]
    # company_table.drop(sep_rows, inplace=True)

    # index = company_table.index.to_list()

    # Get the YOY data for revenue and pat
    # yoy_revenue = company_table['Total revenue'].diff(-1)
    # shifted_revenue = company_table['Total revenue'].shift(-1)
    # company_table.loc[index[1]:, 'YOY_Revenue_percent'] = \
    #     yoy_revenue.iloc[1:] / shifted_revenue.iloc[1:]
    company_table['YOY_Revenue_percent'] = company_table['Total revenue'].pct_change(-1).fillna(0)

    # For pat
    company_table['YOY_PAT_percent'] = company_table['Net income'].pct_change(-1).fillna(0)

    # Get last 5 years data
    last5_revenue = list(company_table['YOY_Revenue_percent'].iloc[-5:])
    last5_pat = list(company_table['YOY_PAT_percent'].iloc[-5:])

    # Check whether last 5 years data is available or set to 0
    for i in range(5 - len(last5_pat)):
        last5_pat.append(0)
    for i in range(5 - len(last5_revenue)):
        last5_revenue.append(0)

    rev = [z * x for z, x in zip(weights, last5_revenue)]
    pat = [z * x for z, x in zip(weights, last5_pat)]
    rev_growth = sum(rev) / sum(weights) * 100
    pat_growth = sum(pat) / sum(weights) * 100

    values = {'Revenue Growth': rev_growth,
              'PAT Growth': pat_growth,
              'CMP': company_info['current_price'],
              'D/E': de,
              'P/E': company_info['pe_ratio'],
              # 'Dividend Yield': company_info['dividend_yield'],
              'ROCE': company_table['ROCE'].iloc[0],
              'ROE': company_table['ROE'].iloc[0],
              'Current Ratio': current_ratio,
              'Quick Ratio': quick_ratio
              }

    try:
        values['P/B'] = company_info['current_price'] / company_info['book_value']
    except:
        values['P/B'] = None
    try:
        values['PEG'] = company_info['pe_ratio'] / pat_growth
    except:
        values['PEG'] = None

    return values