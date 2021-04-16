import plotly.graph_objects as go

def candlestick_chart(dfticker, symbol):
    """ Create a plotly candlestick chart """

    fig = go.Figure(data=[go.Candlestick(x=dfticker['time'],
                open=dfticker['open'],
                high=dfticker['high'],
                low=dfticker['low'],
                close=dfticker['close'])])
    fig.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            # dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
            dict(bounds=[16+5, 9.5+5], pattern="hour"),  # hide hours outside of 9.30am-4pm
            # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
        ],
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='YTD',
                    step='year',
                    stepmode='todate'),
                dict(count=1,
                    label='1y',
                    step='year',
                    stepmode='backward'),
                dict(step='all')
            ])
        ),
        type='date'
    )
    fig.update_layout(
        title=f'{symbol} Stock',
        yaxis_title='Price'
    )
    
    # def zoom(layout, xrange):
        # in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
        # fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]
        # fig.layout.yaxis.range = [100, 500]
    # fig.layout.on_change(zoom, 'xaxis.range')
    return fig