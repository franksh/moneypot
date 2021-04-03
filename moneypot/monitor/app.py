import streamlit as st
import pandas as pd
from moneypot.exchange import get_stocks_list

st.title("Moneypot")

option = st.sidebar.selectbox("Dashboards", ('Stock Overview', '...'), 0)

st.header(option)

stocks = get_stocks_list()
dfstocks = pd.DataFrame(stocks)

st.dataframe(dfstocks)
