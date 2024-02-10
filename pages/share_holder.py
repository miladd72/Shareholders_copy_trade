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

class ShareHolder:
    def __init__(self):
        self.page_initials()
        self.db = SQL()
        self.shares_diff = df_shareholders_change
        self.shares_diff["shareHolderName_"] = self.shares_diff["shareHolderName"] + self.shares_diff["shareHolderCode"].astype(str)


    def page_initials(self):
        st.set_page_config(page_title="Share Holder", page_icon="📈",
                           layout="wide", initial_sidebar_state="expanded")
        st.markdown("# Share Holder")
        st.sidebar.header("Share Holder")

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

    def get_shareholders(self, name, shareholder):
        df = self.shares_diff.query("name == @name and shareHolderName_ == @shareholder")
        # df_feature = FeatureEngineering().calculate_shareholder_features(df)

        cols = ['relatedDate', 'name', 'symbolId', 'countIndividualShareholders', 'percShareIndividual',
                'countCorporateShareholders', 'percShareCorporate', 'totalSharePerc', 'sharePercDiff']
        df_feature = df[cols]

        return df_feature

    def get_data(self, name, share_holder):
        df_feature = self.get_shareholders(name, share_holder)
        df_price = self.get_ohlcv(name)

        df_price["date"] = df_price["relatedDate"].apply(lambda x: pd.to_datetime(x).date())
        df_feature["date"] = df_feature["relatedDate"].apply(lambda x: pd.to_datetime(x).date())

        df_feature1 = pd.merge(df_price[["date"]], df_feature, on="date", how="left")

        df_feature1["sharePercDiff"] = df_feature1["sharePercDiff"].fillna(0)

        return df_price, df_feature1

    def plot_stocks(self, stock_name, share_holder):
        df_price, df_features = self.get_data(stock_name, share_holder)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                            subplot_titles=['Price', 'shareholder change'],
                            row_heights=[3, 1])

        # fig.add_trace(go.Candlestick(x=df_price['date'],
        #                              open=df_price['openPriceAdjust'],
        #                              high=df_price['highPriceAdjust'],
        #                              low=df_price['lowPriceAdjust'],
        #                              close=df_price['closePriceAdjust'],
        #                              increasing_line_color='#006666',
        #                              decreasing_line_color='#FF1940',
        #                              increasing_fillcolor='#006666',  # Blue for bullish candles
        #                              decreasing_fillcolor='#FF1940',
        #                              name='OHLC'), row=1, col=1)

        fig.add_trace(go.Scatter(x=df_price['date'], y=df_price['closePriceAdjust'],
                                 mode='lines', name='closePriceAdjust'), row=1, col=1)

        fig.add_trace(go.Scatter(x=df_features['date'], y=df_features['sharePercDiff'],
                                 mode='lines',  name='sharePercDiff'), row=2, col=1)


        fig.update_layout(height=700, width=1000, xaxis_rangeslider_visible=False, title='Stock and Shareholder difference Chart')

        return fig



    def load_page(self):
        stocks_list = self.shares_diff.name.unique()
        stock = st.sidebar.selectbox("Select Stock Symbol:", stocks_list)

        share_holders_list = self.shares_diff[self.shares_diff.name == stock].shareHolderName_.unique()

        share_holder = st.sidebar.selectbox("Select Share holder:", share_holders_list)

        # breakpoint()
        fig = self.plot_stocks(stock_name=stock, share_holder=share_holder)

        st.plotly_chart(fig)


ShareHolder().load_page()

