import pandas as pd
from bs4 import BeautifulSoup as bs

def create_brsf(raw_data):

    def prepare_data(raw_data):

        def clean_data(data):
            data = data.replace(r'\xa0', '', regex=True)
            data = data.replace({1 : r',', 2 : r','}, '.', regex=True)
            data = data.astype({1 : 'float', 2 : 'float'})
            return data

        soup = bs(raw_data, 'html.parser')
        tables = soup.find_all('table')
        df_tables = pd.read_html(str(tables))

        for table in df_tables:
            if len(table.columns) == 3:
                table = clean_data(table.dropna()).values.tolist()
                if 'A. Przychody' in table[0][0]:
                    profit_n_loss = table
                elif 'Aktywa' in table[0][0]:
                    balance = table

        for i in range(0, len(balance)):
            if 'Pasywa' in balance[i][0]:
                assets = balance[:i]
                liabilities = balance[i:]
                break

        for i in range(0, len(liabilities)):
            if 'Zobowiązania krótkoterminowe' in liabilities[i][0]:
                capital_n_long = liabilities[:i]
                short_liab = liabilities[i:]
                break
        return (profit_n_loss, assets, capital_n_long, short_liab)

    def find_values(data):

        def find_by_keys(keys, data, values):
            for word in keys:
                for i in range(len(data)-1, -1, -1):
                    if word in data[i][0]:
                        values.append(data[i][:2])
                        data.remove(data[i])
                        i -= 1
                        break
                    elif i==0 and (word not in data[i][0]):
                        values.append([word, 0])
            return values

        keys_profit_n_loss = ['A. Przychody', 'C. Zysk (strata)', 'Amortyzacja',
            'Koszty sprzedaży', 'Koszty ogólnego zarządu', 'Odsetki', 'Odsetki',
            'Zysk (strata) brutto', 'Podatek dochodowy', 'Zysk (strata) netto', ]

        keys_assets = ['Aktywa trwałe', 'I. Wartości niematerialne i prawne',
            '2. Wartość firmy', 'Wartość firmy jednostek',
            'Zaliczki na wartości', '1. Środki trwałe', 'Aktywa obrotowe', 'Zapasy',
            'Zaliczki na dostawy', 'z tytułu dostaw i usług', 'z tytułu dostaw i usług',
            'z tytułu dostaw i usług', 'rodki pieniężne i inne aktywa pieniężne', ]

        keys_capital_n_long = [ 'własny', 'podstawowy', 'apitały mniejszości',
        'jemna wartość jednostek', 'odroczonego', '- długoterminowa',
        '- długoterminowe', '- krótkoterminowa', 'krótkoterminowe',
        'Zobowiązania długoterminowe', 'kredyty i pożyczki',
        'inne zobowiązania finansowe', 'zobowiązania wekslowe' ]

        keys_short_liab = [ 'Zobowiązania krótkoterminowe',
        'z tytułu dostaw i usług', 'z tytułu dostaw i usług',
        'z tytułu dostaw i usług', 'kredyty i pożyczki',
        'inne zobowiązania finansowe', 'Ujemna wartość', '- długoterminowe',
        '- krótkoterminowe',
        ]

        values = []
        values = find_by_keys(keys_profit_n_loss, data[0], values)
        values = find_by_keys(keys_assets, data[1], values)
        values = find_by_keys(keys_capital_n_long, data[2], values)
        values = find_by_keys(keys_short_liab, data[3], values)
        return values

    def fill_brsf(values):
        brsf = [
            ['Total Sales', values[0][1] ],
            ['Gross Profit', values[1][1] ],
            ['Net OP. Profit', values[1][1] - values[3][1] - values[4][1] ],
            ['Interest Received', values[6][1] ],
            ['Interest Paid', values[5][1] ],
            ['Other Income/Expense', values[7][1] - values[1][1] + values[3][1]
            + values[4][1]- values[6][1] + values[5][1] ],
            ['Pre Tax Profit', values[7][1] ],
            ['Taxation', values[7][1] - values[9][1] ],
            ['Profit After Tax', values[9][1] ],
            ['Depreciation', values[2][1] ],
            ['Cash & Equivalents', values[22][1] ],
            ['Trade Debtors', values[19][1] + values[20][1] + values[21][1] ],
            ['Stock & Work in Progress', values[17][1] - values[18][1] ],
            ['Tot Curr. Ass.', values[16][1] ],
            ['Tangible Fxed Assets', values[15][1] ],
            ['Intagibles', values[11][1] - values[12][1] - values[14][1] ],
            ['Goodwill', values[12][1] + values[13][1] ],
            ['Total Fix. Ass.' , values[10][1] ],
            ['Overdrafts & STD', values[40][1] + values[41][1] ],
            ['Trade Creditors', values[37][1] + values[38][1] + values[39][1] ],
            ['Tot Curr. Liab.', values[36][1] + values[30][1] + values[31][1]
                + values[44][1] ],
            ['Total Long Term Debt', values[33][1] + values[34][1]
                + values[35][1] ],
            ['Provisions', values[27][1] + values[28][1] + values[29][1] ],
            ['Total LT Liab.', values[32][1] + values[42][1] + values[43][1]
                + values[27][1] + values[28][1] + values[29][1] ],
            ['Share Holders Funds', values[24][1] ],
            ['Retd Earnings/Resvs', values[23][1] - values[24][1]
                + values[25][1] + values[26][1]]
            ]
        rounded_brsf = [[x, round(y)] for x, y in brsf]
        return rounded_brsf

    return fill_brsf(find_values(prepare_data(raw_data)))
