import streamlit as st
import pandas as pd
from moneypot.exchange import get_stocks_list, get_ticker

from moneypot.monitor import candlestick_chart

st.set_page_config(page_title='moneypot',
                        #page_icon = favicon,
                        layout = 'wide', initial_sidebar_state = 'auto')
st.title("Moneypot")

menu_option = st.sidebar.selectbox("Dashboards", ('Stock Overview', 'Ticker'), 1)



def get_stock_label(option):
    return option

if menu_option == 'Stock Overview':
    st.header(menu_option)
    stocks = get_stocks_list(format='dict')
    dfstocks = pd.DataFrame(stocks)

    st.dataframe(dfstocks)


if menu_option == 'Ticker':
    st.header(menu_option)    
    stocks = get_stocks_list(format='dict')
    # stock_names = [stock['name'] for stock in stocks]
    # stock_names = [stock['name'] for stock in stocks]

    dfstocks = pd.DataFrame(stocks)
    # dfstocks['label'] = dfstocks['symbol'] + ' - ' + dfstocks['name']


    # stock_names = tuple(stock['symbol'] + ' - ' + stock['name'] for stock in stocks)
    # stock_ids = tuple(stock['id'] for stock in stocks)

    selected_symbols = st.multiselect("Stock", dfstocks[['symbol', 'id']], format_func=get_stock_label)

    tickers = {}
    for symbol in selected_symbols:
        stock_id = dfstocks[dfstocks['symbol']==symbol]['id'].values[0]

        # st.write(type(stock_id))
        ticker = get_ticker(stock_id, format='dict')
        dfticker = pd.DataFrame(ticker)
        # st.write(dfticker.head())

        fig = candlestick_chart(dfticker, symbol)

        st.plotly_chart(fig)
        # fig.show()
        # st.write(ticker)
    # stocks = get_stocks_list(format='dict')
    # dfstocks = pd.DataFrame(stocks)

    # st.dataframe(dfstocks)
