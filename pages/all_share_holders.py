import streamlit as st
from datetime import datetime, timedelta
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

from app.get_data import SQL
from app import df_shareholders_change
from app.configs import TABLE_PRICE
from app.process import FeatureEngineering

class ShareHolders:
    def __init__(self):
        self.page_initials()
        self.db = SQL()
        self.shares_diff = df_shareholders_change

    def page_initials(self):
        st.set_page_config(page_title="Share Holders", page_icon="📈",
                           layout="wide", initial_sidebar_state="expanded")
        st.markdown("# Share Holders")
        st.sidebar.header("Share Holders")

    @st.cache_data
    def get_ohlcv(_self, name):
        obj = SQL()

        symbol_id = _self.shares_diff.loc[_self.shares_diff["name"] == name, "symbolId"].iloc[0]

        columns_to_select = [
            'volumeTrades',
            'valueTrades',
            'symbolId',
            'relatedDate',
            'symbolHistoryId',
            'closePriceAdjust',
            'highPriceAdjust',
            'lastPriceAdjust',
            'lowPriceAdjust',
            'openPriceAdjust',
            'yestPriceAdjust'
        ]

        filters_to_apply = [
            ('tradeType', '=', 1),
            ('symbolId', '=', symbol_id),
        ]

        sort_order = ['relatedDate DESC']

        result_df = obj.get_data(
            table_name=TABLE_PRICE,
            columns=columns_to_select,
            filters=filters_to_apply,
            sort=sort_order
        )

        return result_df

    def get_shareholders(self, name):
        df = self.shares_diff.query("name == @name")
        # df_feature = FeatureEngineering().calculate_shareholder_features(df)

        cols = ['relatedDate', 'name', 'symbolId', 'countIndividualShareholders', 'percShareIndividual',
                'countCorporateShareholders', 'percShareCorporate', 'totalSharePerc']
        df_feature = df[cols].drop_duplicates(keep="first")

        return df_feature

    def get_data(self, name, from_date=None, to_date=None):
        df_feature = self.get_shareholders(name)
        df_price = self.get_ohlcv(name)

        df_price["date"] = df_price["relatedDate"].apply(lambda x: pd.to_datetime(x).date())
        df_feature["date"] = df_feature["relatedDate"].apply(lambda x: pd.to_datetime(x).date())

        df_feature1 = pd.merge(df_price[["date"]], df_feature, on="date", how="outer")
        df_feature1 = df_feature1.ffill()
        min_price_date = df_price.date.min()
        df_feature1 = df_feature1.query("date >= @min_price_date")

        df_feature1 = df_feature1.dropna()

        if not(from_date is None and to_date is None):
            df_price = df_price.query("date >= @from_date and date <= @to_date")
            df_feature1 = df_feature1.query("date >= @from_date and date <= @to_date")

        return df_price, df_feature1

    def plot_stocks(self, stock_name, from_date, to_date):
        df_price, df_features = self.get_data(stock_name, from_date, to_date)

        fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                            subplot_titles=['Price', 'percent of shareholders',
                                            'number of shareholders', 'sum of shareholders'],
                            row_heights=[5, 2, 2, 2])

        fig.add_trace(go.Candlestick(x=df_price['date'],
                                     open=df_price['openPriceAdjust'],
                                     high=df_price['highPriceAdjust'],
                                     low=df_price['lowPriceAdjust'],
                                     close=df_price['closePriceAdjust'],
                                     increasing_line_color='#006666',
                                     decreasing_line_color='#FF1940',
                                     increasing_fillcolor='#006666',  # Blue for bullish candles
                                     decreasing_fillcolor='#FF1940',
                                     name='OHLC'), row=1, col=1)

        # fig.add_trace(go.Scatter(x=df_price['date'], y=df_price['closePriceAdjust'],
        #                          mode='lines', name='closePriceAdjust'), row=1, col=1)

        fig.add_trace(go.Scatter(x=df_features['date'], y=df_features['percShareIndividual'],
                                 mode='lines',  name='percShareIndividual'), row=2, col=1)
        fig.add_trace(go.Scatter(x=df_features['date'], y=df_features['percShareCorporate'],
                                 mode='lines', name='percShareCorporate'), row=2, col=1)

        fig.add_trace(go.Scatter(x=df_features['date'], y=df_features['countIndividualShareholders'],
                                 mode='lines', name='countIndividualShareholders'), row=3, col=1)
        fig.add_trace(go.Scatter(x=df_features['date'], y=df_features['countCorporateShareholders'],
                                 mode='lines', name='countCorporateShareholders'), row=3, col=1)

        fig.add_trace(go.Scatter(x=df_features['date'], y=df_features['totalSharePerc'],
                                 mode='lines',name='totalSharePerc'), row=4, col=1)

        fig.update_layout(height=900, width=1200, xaxis_rangeslider_visible=False, title='Stock and Shareholders feature Chart')

        return fig



    def load_page(self):
        stocks_list = self.shares_diff.name.unique()
        stock = st.sidebar.selectbox("Select Stock Symbol:", stocks_list)

        st.sidebar.subheader("Select Date Range:")

        from_date = st.sidebar.date_input("Start Date", value=datetime.now().date() - timedelta(days=1500))
        to_date = st.sidebar.date_input("Stop Date", value=datetime.now().date())

        # breakpoint()
        fig = self.plot_stocks(stock_name=stock, from_date=from_date, to_date=to_date)

        st.plotly_chart(fig)


ShareHolders().load_page()

# ShareHolders().get_data("کپشیر")
