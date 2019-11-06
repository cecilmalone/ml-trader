import matplotlib.pyplot as plt
from coinmarketcap import Market
import pandas as pd
import time

def recebe_btc(lista):
    market = Market()
    ticker = market.ticker(convert='BRL')
    data = ticker['data']
    
    btc = data['1']['quotes']['BRL']['price']
    
    lista.append(btc)
    return lista

def recebe_xrp(lista):
    market = Market()
    ticker = market.ticker(convert='BRL')
    data = ticker['data']
    
    xrp = data['52']['quotes']['BRL']['price']
    
    lista.append(xrp)
    return lista
    
lista_btc = []
lista_xrp = []

#BTC
fig_btc = plt.figure(figsize=(10, 10))
ax_btc = fig_btc.gca()

#XRP
fig_xrp = plt.figure(figsize=(10, 10))
ax_xrp = fig_xrp.gca()

while True:
    ax_btc.clear()
    ax_xrp.clear()
    ax_btc.plot(recebe_btc(lista_btc))
    ax_xrp.plot(recebe_xrp(lista_xrp))
    plt.pause(1)
    #time.sleep(1)