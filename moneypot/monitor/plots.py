import altair as alt
import plotly.graph_objects as go

def lightweight_candlestick_chart(dfticker, symbol, priceScaleMode='IndexedTo100'):
    """

    Parameters:
    -----------
     - priceScaleMode: string
        One of: Normal, Logarithmic, Percentage, IndexedTo100
        - 
    """

    data_json = dfticker[['time', 'open', 'high', 'low', 'close']].to_json(orient='records', date_format='epoch', date_unit='s')
    # print(data_json)
    import streamlit.components.v1 as components
    # attrs_plot = {
    #     'priceScaleMode': priceScaleMode
    # }
    comp = components.html("""
        <script type="text/javascript" src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
        <div class='lightchart'>
            <script>
            const chart = LightweightCharts.createChart(document.body,
            { 
                width: 600, 
                height: 300,
                localization: { locale: 'en-US' },
                priceScale: {
                    mode: """ + f"LightweightCharts.PriceScaleMode.{priceScaleMode}," + \
                    """autoScale: true
                }
            });
            const candlestickSeries = chart.addCandlestickSeries();

        """ + """
            candlestickSeries.setData({})
        """.format(data_json) \
        +"""
            console.log(LightweightCharts);
            </script>
        </div>
        """,
        height=300
    )
    return comp


def lightweight_line_chart(dfticker, symbol):

    data_json = dfticker.rename(columns={'close': 'value'})[['time', 'value']].to_json(orient='records')

    import streamlit.components.v1 as components
    comp = components.html("""
        <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
        <div class='lightchart'>
            <script>
            const chart = LightweightCharts.createChart(document.body,
                                            { width: 500, height: 300 });
            const lineSeries = chart.addLineSeries();

        """ + """
            lineSeries.setData({})</script></div>
        """.format(data_json),
        height=600
    )
    return comp


def candlestick_chart(dfticker, symbol):
    color_green = "#3D9970"
    color_red = "#FF4136"
    open_close_color = alt.condition("datum.open <= datum.close",
                                    alt.value(color_green),
                                    alt.value(color_red))

    brush = alt.selection(type='interval', encodings=['x'])

    base = alt.Chart(dfticker).encode(
        x=alt.X('time:T',
        ),
    )

    rule = base.mark_rule().encode(
        x=alt.X(
            'time:T',
            scale=alt.Scale(domain=brush)),
        y=alt.Y(
            'low:Q',
            title='Price',
            scale=alt.Scale(zero=False),
        ),
        y2=alt.Y2('high:Q')
    )
    bar = base.mark_bar().encode(
        x=alt.X(
            'time:T',
            scale=alt.Scale(domain=brush)),
        y=alt.Y('open:Q', scale=alt.Scale(zero=False)),
        y2=alt.Y2('close:Q'),
        # tooltip='time',
        color=open_close_color
    )

    line = base.mark_square(color='black').encode(
        x=alt.X('time:T',
                axis=alt.Axis(
                        # format='%m/%d',
                        labelAngle=-45,
                        title='time',
                        ticks=True
                    ),
                ),
        y=alt.Y(
            'close:Q',
            scale=alt.Scale(zero=False)),
            # color=alt.Color('black')),
    )

    chart_view = (rule + bar).encode(
        x=alt.X(
            'time:T',
            scale=alt.Scale(domain=brush, nice=True),
        ),
    ).properties(width=700, height=300).interactive(bind_x=False, bind_y=True)

    chart_select = line.add_selection(brush).properties(width=800, height=50)
    chart_final = alt.vconcat(chart_view, chart_select)

    return chart_final


def candlestick_chart_plotly(dfticker, symbol):
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