# from functools import wraps
# from matplotlib import colors
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

symbol_list = []
contract_code_list = []
fee_list = []


def fee_plt(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        # df = []
        df = pd.DataFrame(
            {'symbol': symbol_list, 'fee': fee_list})
        df = df.sort_values('fee')
        df = df[:5].append(df[-5:].sort_values('fee'))
        plt.figure(figsize=(18, 18), dpi=60)
        # plt.rcParams['axes.unicode_minus']=False
        plt.bar(
            df['symbol'],
            df['fee'],
            width=0.8,
            color=color
        )
        for i, val in enumerate(df['fee'].values):
            if val < 0:
                plt.text(
                    i,
                    val,
                    float(val),
                    fontdict={
                        'fontweight': 150,
                        'size': 17},
                    verticalalignment='top',
                    horizontalalignment='center')
            else:
                plt.text(
                    i,
                    val,
                    float(val),
                    fontdict={
                        'fontweight': 150,
                        'size': 17},
                    verticalalignment='bottom',
                    horizontalalignment='center')

        def to_percent(temp, position):
            return '%1.0f' % (100 * temp) + '%'
        plt.gca().yaxis.set_major_formatter(
            FuncFormatter(to_percent))
        plt.gca().spines['right'].set_color('none')
        plt.gca().spines['top'].set_color('none')
        # 用来正常显示中文标签
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.title(
            ex + '费率统计',
            fontsize=50,
            color='R',
            loc='left')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        return func(*args, **kwargs)
    return wrapper


@fee_plt
def get_huobi_fee(url_info, symbol,
                  contract_code, url_rate, rate):
    global ex
    ex = '火币'
    global color
    color = 'Y'
    swap_all = requests.get(url_info).json()[
        'data']  # 获得所有币种列表数据
    # 刷选币种，获得交易对列表
    for i in range(len(swap_all)):
        if swap_all[i][symbol] not in symbol_list:
            symbol_list.append(swap_all[i][symbol])
            contract_code_list.append(
                swap_all[i][contract_code])
    # 获得手续费列表数据
    for x in range(len(symbol_list)):
        fee = requests.get(
            url_rate +
            contract_code_list[x]).json()['data'][rate]
        fee = float(fee) * 100
        fee = float('%.5f' % fee)
        fee_list.append(fee)
    return fee_list


@fee_plt
def get_ftx_fee(url_info, symbol,
                contract_code, url_rate, rate):
    global symbol_list
    symbol_list = []
    global contract_code_list
    contract_code_list = []
    global fee_list
    fee_list = []
    global ex
    ex = 'FTX'
    global color
    color = 'R'
    swap_all = requests.get(url_info).json()['result']
    for i in range(len(swap_all)):
        if swap_all[i][symbol] not in symbol_list and 'PERP' in swap_all[i][contract_code]:
            symbol_list.append(swap_all[i][symbol])
            contract_code_list.append(
                swap_all[i][contract_code])
    for x in range(len(symbol_list)):
        fee = requests.get(
            url_rate +
            contract_code_list[x]).json()['result'][1][rate]
        fee = float(fee) * 100
        fee = float('%.5f' % fee)
        fee_list.append(fee)
    return fee_list


@fee_plt
def get_binance_fee(url_info, symbol,
                    contract_code, url_rate, rate):
    global symbol_list
    symbol_list = []
    global contract_code_list
    contract_code_list = []
    global fee_list
    fee_list = []
    global ex
    ex = '币安'
    global color
    color = 'B'
    swap_all = requests.get(url_info).json()['symbols']
    for i in range(len(swap_all)):
        if swap_all[i][symbol] not in symbol_list:
            symbol_list.append(swap_all[i][symbol])
            contract_code_list.append(
                swap_all[i][contract_code])
    for x in range(len(symbol_list)):
        fee = requests.get(
            url_rate +
            contract_code_list[x]).json()[rate]
        fee = float(fee) * 100
        fee = float('%.5f' % fee)
        fee_list.append(fee)
    return fee_list


@fee_plt
def get_okex_fee(url_info, symbol,
                 contract_code, url_rate, rate):
    global symbol_list
    symbol_list = []
    global contract_code_list
    contract_code_list = []
    global fee_list
    fee_list = []
    global ex
    ex = 'OK'
    global color
    color = 'G'
    swap_all = requests.get(url_info).json()
    for i in range(len(swap_all)):
        if swap_all[i][symbol] not in symbol_list:
            symbol_list.append(swap_all[i][symbol])
            contract_code_list.append(
                swap_all[i][contract_code])
    for x in range(len(symbol_list)):
        fee = requests.get(
            url_rate +
            contract_code_list[x] +
            '/funding_time').json()[rate]
        fee = float(fee) * 100
        fee = float('%.5f' % fee)
        fee_list.append(fee)
    return fee_list


if __name__ == "__main__":

    while True:
        inn = input(
            '要查询哪个交易所费率：1：火币；2：ftx；3：币安；4：okex；5：全部' +
            '\n')
        if inn == '1':
            get_huobi_fee(
                url_info='https://api.hbdm.com/swap-api/v1/swap_contract_info',
                symbol='symbol',
                contract_code='contract_code',
                url_rate='https://api.hbdm.com/swap-api/v1/swap_funding_rate?contract_code=',
                rate='funding_rate')
            break
        elif inn == '2':
            get_ftx_fee(
                url_info='https://ftx.com/api/futures',
                symbol='underlying',
                contract_code='name',
                url_rate='https://ftx.com/api/funding_rates?future=',
                rate='rate')
            break
        elif inn == '3':
            get_binance_fee(
                url_info='https://fapi.binance.com/fapi/v1/exchangeInfo',
                symbol='baseAsset',
                contract_code='symbol',
                url_rate='https://fapi.binance.com/fapi/v1/premiumIndex?symbol=',
                rate='lastFundingRate')
            break
        elif inn == '4':
            get_okex_fee(
                url_info='https://www.okex.com/api/swap/v3/instruments',
                symbol='underlying_index',
                contract_code='instrument_id',
                url_rate='https://www.okex.com/api/swap/v3/instruments/',
                rate='funding_rate')
            break
        elif inn == '5':
            get_huobi_fee(
                url_info='https://api.hbdm.com/swap-api/v1/swap_contract_info',
                symbol='symbol',
                contract_code='contract_code',
                url_rate='https://api.hbdm.com/swap-api/v1/swap_funding_rate?contract_code=',
                rate='funding_rate')
            get_ftx_fee(
                url_info='https://ftx.com/api/futures',
                symbol='underlying',
                contract_code='name',
                url_rate='https://ftx.com/api/funding_rates?future=',
                rate='rate')
            get_binance_fee(
                url_info='https://fapi.binance.com/fapi/v1/exchangeInfo',
                symbol='baseAsset',
                contract_code='symbol',
                url_rate='https://fapi.binance.com/fapi/v1/premiumIndex?symbol=',
                rate='lastFundingRate')
            get_okex_fee(
                url_info='https://www.okex.com/api/swap/v3/instruments',
                symbol='underlying_index',
                contract_code='instrument_id',
                url_rate='https://www.okex.com/api/swap/v3/instruments/',
                rate='funding_rate')
            break
        else:
            print('睇清楚，傻hi')
    plt.show()
