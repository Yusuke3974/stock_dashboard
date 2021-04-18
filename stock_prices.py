import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('ビックテック（FANGAM）株価ダッシュボード')

st.sidebar.write("""
# FANGAM株価
ビックテックと呼ばれるテクノロジー系企業の株価可視化ツールです。
""")

days = st.sidebar.slider('日数', 1,50,25)

st.write(f'''
### 直近、 **{days}日間** のFANGAM株価
''')

@st.cache
def get_data(days,tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df,hist])
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください',
        0.0,3500.0, (0.0, 3500.0)
    )

    tickers = {
        'apple':'AAPL',
        'google' :'GOOGL',
        'facebook':'FB',
        'amazon':'AMZN',
        'microsoft':'MSFT',
        'netflix':'NFLX'
    }

    df = get_data(days,tickers)

    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['apple','google','facebook','amazon','microsoft','netflix']
    )

    if not companies:
        st.error('少なくとも１社は選んでください。')
    else:
        data = df.loc[companies]
        st.write('# 株価',data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data,id_vars=['Date']).rename(columns={'value':'STOCK PRICE(USD)'})

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x='Date:T',
                y=alt.Y('STOCK PRICE(USD):Q',stack=None),
                color='Name:N'
            )
        )

        st.altair_chart(chart,use_container_width=True)
    
except:
    st.error(
        "エラーが起きています。"
    )