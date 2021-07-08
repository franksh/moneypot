import streamlit as st
import altair as alt
import pandas as pd
from moneypot.database import get_all_stocks, get_ticker_stock, get_all_coins, get_ticker_coin

from moneypot.monitor import candlestick_chart, lightweight_line_chart, lightweight_candlestick_chart

st.set_page_config(page_title='moneypot',
                        #page_icon = favicon,
                        layout = 'wide', initial_sidebar_state = 'auto')
st.title("Moneypot")

menu_option = st.sidebar.selectbox("Dashboards", ('Stock Overview', 'Ticker Stocks', 'Coin Overview', 'Ticker Coins'), 1)



def get_stock_label(option):
    return option

if menu_option == 'Stock Overview':
    st.header(menu_option)
    dfstocks = get_all_stocks()
    st.dataframe(dfstocks)

if menu_option == 'Coin Overview':
    st.header(menu_option)
    dfcoins = get_all_coins()
    st.dataframe(dfcoins)

if menu_option == 'Ticker Stocks':
    st.header(menu_option)    
    dfstocks = get_all_stocks()
    # stock_names = [stock['name'] for stock in stocks]
    # stock_names = [stock['name'] for stock in stocks]

    # dfstocks['label'] = dfstocks['symbol'] + ' - ' + dfstocks['name']


    # stock_names = tuple(stock['symbol'] + ' - ' + stock['name'] for stock in stocks)
    # stock_ids = tuple(stock['id'] for stock in stocks)
    # dfstocks = pd.DataFrame([ s.__dict__ for s in stocks ])

    selected_symbols = st.multiselect("Stock", dfstocks[['symbol', 'id']], format_func=get_stock_label)

    # Plot options
    col1, col2, col3 = st.beta_columns(3)
    chart_priceScaleMode = col1.selectbox("Price Scale", ['Normal', 'Logarithmic', 'Percentage', 'IndexedTo100'])

    chart_timeInterval = col2.selectbox("Time Interval", ['15min', '1H', '1D', '1W'])

    tickers = {}
    for symbol in selected_symbols:
        stock = dfstocks.loc[dfstocks['symbol']==symbol]
        stock_id = stock['id'].item()
        stock_name = stock['name'].item()
        
# dfticker.resample_time('1min')
        # stock_id = dfstocks[dfstocks['symbol']==symbol]['id'].values[0]

        # st.write(type(stock_id))
        # ticker = get_ticker(stock_id, format='dict')
        # dfticker = pd.DataFrame(ticker)
        # st.write(dfticker.head())
        dfticker = get_ticker_stock(stock_id)
        dfticker = dfticker.resample_time(chart_timeInterval)

        # Plotly chart
        # fig = candlestick_chart(dfticker, symbol)
        # st.plotly_chart(fig)
        
        # Streamlit chart
        # c = alt.Chart(dfticker).mark_circle().encode(
        #     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

        # Candlestick chart
        # chart = candlestick_chart(dfticker, symbol)
        # st.altair_chart(chart)

        # lightweight_line_chart(dfticker, symbol)
        st.write(stock_name)
        lightweight_candlestick_chart(dfticker, symbol,
            priceScaleMode=chart_priceScaleMode)



if menu_option == 'Ticker Coins':
    st.header(menu_option)    
    dfstocks = get_all_coins()
    # stock_names = [stock['name'] for stock in stocks]
    # stock_names = [stock['name'] for stock in stocks]

    # dfstocks['label'] = dfstocks['symbol'] + ' - ' + dfstocks['name']


    # stock_names = tuple(stock['symbol'] + ' - ' + stock['name'] for stock in stocks)
    # stock_ids = tuple(stock['id'] for stock in stocks)
    # dfstocks = pd.DataFrame([ s.__dict__ for s in stocks ])

    selected_symbols = st.multiselect("Coin", dfstocks[['symbol']])

    # Plot options
    col1, col2, col3 = st.beta_columns(3)
    chart_priceScaleMode = col1.selectbox("Price Scale", ['Normal', 'Logarithmic', 'Percentage', 'IndexedTo100'])

    chart_timeInterval = col2.selectbox("Time Interval", ['15min', '1H', '1D', '1W'])

    tickers = {}
    for symbol in selected_symbols:
        # stock = dfstocks.loc[dfstocks['symbol']==symbol]
        # stock_id = stock['id'].item()
        # stock_name = stock['name'].item()
        
# dfticker.resample_time('1min')
        # stock_id = dfstocks[dfstocks['symbol']==symbol]['id'].values[0]

        # st.write(type(stock_id))
        # ticker = get_ticker(stock_id, format='dict')
        # dfticker = pd.DataFrame(ticker)
        # st.write(dfticker.head())
        dfticker = get_ticker_coin(symbol)
        dfticker = dfticker.resample_time(chart_timeInterval)

        # coin chart
        # fig = candlestick_chart(dfticker, symbol)
        # st.plotly_chart(fig)
        
        # Streamlit chart
        # c = alt.Chart(dfticker).mark_circle().encode(
        #     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

        # Candlestick chart
        # chart = candlestick_chart(dfticker, symbol)
        # st.altair_chart(chart)

        # lightweight_line_chart(dfticker, symbol)
        lightweight_candlestick_chart(dfticker, symbol,
            priceScaleMode=chart_priceScaleMode)