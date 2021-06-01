import numpy as np


def get_intrinsic_value(fcf=100.0 * 1e7, g1=0.15, g2=0.10, n1=5, n2=5, nf=100,
                    r=0.07, t=0.02, mcap=10000.0 * 1e7, cmp=100.0,
                    debt=0.0, mos=0.10):
    """
    Calculating intrinsic value based on discounted cash flow model
    Parameters
    ---------
        fcf : float, default = 100.0*1e7
            Initial Free cash flow

        g1 : float, default = 0.15
            Growth rate for period 1

        g2 : float, default = 0.10
            Growth rate for period 2

        n1 : int, default = 5
            Number of Years in period 1

        n2 : int, default = 5
            Number of Years in period 2

        nf : int, default = 100
            Number of Years for terminal period

        r : float, default = 0.07
            The Discount Rate: This is the assured rate of return on the
            safest security.

        t : float, default = 0.02
            The Terminal rate: THe rate of growth after (n1+n2) years

        mcap : float, default = 10000.0*1e7
            The market cap of the company

        cmp : float, default = 100.0
            The current market price of the share

        debt : float, default = 0.0
            The net debt of the company

        mos : float, default = 0.10
            The Margin of safety

    Returns
    ---------
        iv : float
            The intrinsic value per share of the company
    """

    dps = debt / mcap * cmp
    fcfps = fcf / mcap * cmp
    A1 = (1 + g1) / (1 + r)
    A2 = (1 + g2) / (1 + r)
    B = (1 + t) / (1 + r)
    gv1 = fcfps * A1 * (1 - A1 ** n1) / (1 - A1)
    gv2 = fcfps * A1 ** n1 * A2 * (1 - A2 ** n2) / (1 - A2)
    terminal_value = fcfps * A1 ** n1 * A2 ** n2 * B * (1 - B ** nf) / (1 - B)
    iv = (gv1 + gv2 + terminal_value - dps) * (1 - mos)

    return iv


def intrinsic_value(company_table, company_info):
    # Get the intrinsic value
    cf_operating = company_table['Net cash provided by operating activities']
    try:
        cf_fixed_purchased = company_table['Investments in property, plant and equipment']
    except KeyError:
        cf_fixed_purchased = 0
    # try:
    #     cf_fixed_sold = company_table['FixedAssetsSold']
    # except KeyError:
    #     cf_fixed_sold = 0
    free_cf = cf_operating + cf_fixed_purchased #+ cf_fixed_sold

    free_cf = free_cf.reindex(index=free_cf.index[::-1])
    fcf_initial = free_cf.iloc[-3:].mean()
    num_years = 4
    try:
        fit = np.polyfit(np.arange(0, len(free_cf.iloc[-num_years:])), free_cf.iloc[-num_years:], 1)
        slope = fit[0] / free_cf.iloc[-num_years:].max()
        if free_cf.iloc[-num_years+1] < 0:
            slope = 0.10
    except:
        slope = 0.10
        print(free_cf)

    # print(free_cf.iloc[-num_years:])
    # print(fcf_initial)
    # print(fit[0])
    # print('Slope = ', fit[0], ", ", "Intercept = ", fit[1])




    int_value = get_intrinsic_value(fcf=fcf_initial * 1e7,
                                    g1=slope, g2=slope/2,
                                    mcap=company_info['market_cap'] * 1e7,
                                    cmp=company_info['current_price'],
                                    debt=company_table['Long-term debt'].iloc[-1] * 1e7)

    return int_value, slope


#%%
if __name__ == "__main__":
    fcf = 114930000*1000/1e7
    ivh, growth_rate= get_intrinsic_value(fcf, mcap=255492, cmp=942)
    print(ivh)
