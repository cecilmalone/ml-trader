import requests, json
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import numpy as np

janela = 100
desvio = 1.8

historico_bid = []
historico_ask = [] 
historico_lower_band = []
historico_upper_band = []
historico_compras = []
historico_vendas = []
historico_sinal = []
index_compras = []
index_vendas = []

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

def bollinger_bands(bid, ask, janela, desvio):
    if len(bid) > janela:
        media = bid.rolling(window = janela).mean()
        rolling_std = bid.rolling(window = janela).std()
        upper_band = media + (rolling_std * desvio)
        lower_band = media - (rolling_std * desvio)
        
        porcentagem = spread(bid[-1:], ask[-1:])
        diferenca = ask[-1:] - bid[-1:]
        
        ax.text(len(ask) + (len(ask)/10), bid[-1:] + (diferenca/2), 'Spread ' + str(np.around(float(porcentagem), 4)) + '%')
        
        ax.plot(upper_band, '--', color='blue', alpha=.5)
        ax.plot(lower_band, '--', color='blue', alpha=.3)
    
        ax.scatter(len(ask), upper_band[-1:], color='green', alpha=.1)
        ax.scatter(len(ask), lower_band[-1:], color='green', alpha=.1)
    else:
        print('Sem dados suficientes para criar faixas de Bollinger')
        
def detect_cross(bid, ask, lower_band, upper_band, index):
    historico_bid.append(bid)
    historico_ask.append(ask)
    historico_lower_band.append(lower_band)
    historico_upper_band.append(upper_band)
    
    del historico_bid[:-10]
    del historico_ask[:-10]
    del historico_lower_band[:-10]
    del historico_upper_band[:-10]
    
    if len(historico_sinal) > 1:
        if historico_bid[-1:] > historico_lower_band[-1:] and historico_bid[-2:-1] <= historico_lower_band[-2:-1]:
            historico_compras.append(float(ask))
            index_compras.append(index)
            sinal = 'Buy'
            sinal_action = 1
        elif historico_bid[-1:] < historico_upper_band[-1:] and historico_bid[-2:-1] >= historico_upper_band[-2:-1]:
            historico_vendas.append(float(bid))
            index_vendas.append(index)
            sinal = 'Sell'
            sinal_action = 2
        else:
            sinal = 'Hold'
            sinal_action = 0
            
        historico_sinal.append(sinal_action)
    else:
        sinal = 'Hold'
        sinal_action = 0
        historico_sinal.append(sinal_action)
        
    return lower_band, upper_band

def reset_memoria():
    global historico_compras, historico_vendas, index_compras, index_vendas
    
    historico_compras = []
    historico_vendas = []
    index_compras = []
    index_vendas = []

def plot_negociatas(bid, ask, lower_band, upper_band):
    reset_memoria()
    
    for i in range(len(bid) - (janela * 2), len(bid)):
        _ = detect_cross(float(bid[i]), float(ask[i]), float(lower_band[i]), float(upper_band[i]))
        
    if len(historico_compras) > 0:
        ax.scatter(index_compras, historico_compras, marker='v', color='red')
        for c in range(len(index_compras)):
            ax.text(index_compras[c], historico_compras[c], ' - compra', color='black', alpha=.5)
            
    if len(historico_vendas) > 0:
        ax.scatter(index_vendas, historico_vendas, marker='^', color='green')
        for v in range(len(index_vendas)):
            ax.text(index_vendas[v], historico_vendas[v], ' - venda', color='black', alpha=.5)
    
def main():
    df = pd.read_csv('tickers.csv')
    if len(df) > 1:
        ax.clear()
        bid = df['bid']
        ask = df['ask']
        
        diferenca = ask[-1:] - bid[-1:]
        
        plt.title('Bitcoin / USD')
        
        if len(bid) < (janela * 2):
            ax.set_xlim(0, len(bid) + (len(bid)/10))
        else:
            ax.set_xlim(len(bid) - (janela * 2), len(bid) + 10)
            bid_min = np.array(bid[-janela*2:]).min()
            ask_max = np.array(ask[-janela*2:]).max()
            ax.set_ylim(bid_min - (bid_min * 0.01), ask_max + (ask_max * 0.01))
        
        ax.plot(bid, label='BID - Venda BTC ' + str(np.around(float(bid[-1:]), 8)), color='black', alpha=.5)
        ax.plot(ask, label='ASK - Compra BTC ' + str(np.around(float(ask[-1:]), 8)), color='gray', alpha=.5)
        
        if len(bid) > (janela * 2):
            lower_band, upper_band = bollinger_bands(bid, ask, janela, desvio)
            plot_negociatas(bid, ask, lower_band, upper_band)
        plt.pause(2)
        
while True:
    try:
        get_tickers()
    except:
        print('Problemas na conexão')
        time.sleep(5)
        
    try:
        main()
    except:
        print('Encerrando o programa')
        exit()