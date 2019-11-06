import requests, json
import matplotlib.pyplot as plt
import pandas as pd
import time

fig = plt.figure(figsize=(10,10))
ax = fig.gca()

grava = open('tickers.csv', 'w')
grava.write('bid,ask\n')
grava.close()

def get_tickers():
    bitfinex_ltc = 'https://api.bitfinex.com/v1/pubticker/ltcbtc'
    data_bitfinex_ltc = requests.get(url=bitfinex_ltc)
    binary_bitfinex_ltc = data_bitfinex_ltc.content
    output_bitfinex_ltc = json.loads(binary_bitfinex_ltc)
    
    grava = open('tickers.csv', 'a')
    grava.write(str(output_bitfinex_ltc['bid']) + ',' + str(output_bitfinex_ltc['ask']) + '\n')
    grava.close()
    
def plot():
    df = pd.read_csv('tickers.csv')
    
    if len(df) > 1:
        bid = df['bid']
        ask = df['ask']
        ax.clear()
        ax.plot(bid, label = "Bid - Venda LTC "+str(float(bid[-1:])))
        ax.plot(ask, label = "Ask - Compra LTC "+str(float(ask[-1:])))
        plt.legend()
        plt.pause(2)
        
while True:
    try:
        get_tickers()
    except:
        print('Erro no servidor')
        time.sleep(5)
        
    try:
        plot()
    except:
        print('Erro na plotagem')
        time.sleep(1)