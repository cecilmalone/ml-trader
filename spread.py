import requests, json
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import numpy as np

janela = 30
desvio = 2

existe = os.path.isfile('tickers.csv')

if not existe:
    grava = open('tickers.csv', 'w')
    grava.write('bid,ask\n')
    grava.close()

fig = plt.figure(figsize=(10,10))
ax = fig.gca()

def get_tickers():
    bitfinex_ltc = 'https://api.bitfinex.com/v1/pubticker/ltcbtc'
    data_bitfinex_ltc = requests.get(url=bitfinex_ltc)
    binary_bitfinex_ltc = data_bitfinex_ltc.content
    output_bitfinex_ltc = json.loads(binary_bitfinex_ltc)
    
    grava = open('tickers.csv', 'a')
    grava.write(str(output_bitfinex_ltc['bid']) + ',' + str(output_bitfinex_ltc['ask']) + '\n')
    grava.close()
    
def spread(bid, ask):
    porcento = ask / 100
    diferenca = ask - bid
    porcentagem = diferenca / porcento
    
    return porcentagem

def bollinger_bands(tickers, janela, desvio):
    if len(tickers) > janela:
        media = tickers.rolling(window = janela).mean()
        rolling_std = tickers.rolling(window = janela).std()
        upper_band = media + (rolling_std * desvio)
        lower_band = media - (rolling_std * desvio)
        
        return media, upper_band, lower_band

def plot():
    df = pd.read_csv('tickers.csv')
    if len(df) > 1:
        ax.clear()
        bid = df['bid']
        ask = df['ask']
        
        diferenca = ask[-1:] - bid[-1:]
        
        plt.title('Litecoin / BTC')
        ax.set_xlim(len(bid)/10, len(bid)+(len(bid)/4)+5)
        ax.plot(bid, label='BID - Venda LTC ' + str(np.around(float(bid[-1:]), 8)), color='green', alpha=.5)
        ax.plot(ask, label='ASK - Compra LTC ' + str(np.around(float(ask[-1:]), 8)), color='red', alpha=.5)
        
        media, upper_band, lower_band = bollinger_bands(bid, janela, desvio)
        ax.plot(media, '--', color='gray', label='SMA ' + str(janela))
        
        porcentagem = spread(bid[-1:], ask[-1:])
        ax.text(len(ask) + (len(ask)/10), bid[-1:] + (diferenca/2), 'Spread ' + str(np.around(float(porcentagem), 4)) + '%')
           
        plt.legend()
        
        ax.plot(upper_band, '--', color='blue', alpha=.5)
        ax.plot(lower_band, '--', color='blue', alpha=.3)
        
        plt.pause(2)
        
while True:
    try:
        get_tickers()
    except:
        print('Problemas na conexão')
        time.sleep(5)
        
    try:
        plot()
    except:
        print('Encerrando o programa')
        exit()