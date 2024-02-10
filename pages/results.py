import streamlit as st
import os
import pandas as pd

from app.configs import ROOT_DIR

class Results:
    def __init__(self):
        self.page_initials()
        self.df_result = pd.read_csv(os.path.join(ROOT_DIR, "result.csv"), index_col=False)

    def page_initials(self):
        st.set_page_config(page_title="Results", page_icon="📈",
                           layout="wide", initial_sidebar_state="expanded")
        st.markdown("# Best Share Holder")
        # st.sidebar.header("Share Holders")

    def get_result(self):
        df_result = self.df_result
        cols = ['avg_1_Week_Return', 'avg_1_Month_Return', 'avg_3_Month_Return',
                'avg_6_Month_Return', 'avg_1_Year_Return']
        df_result[cols] = df_result[cols] * 100
        return df_result

    def show_results(self, period):
        df_result = self.get_result()

        if period == "1Week":
            df = df_result.sort_values(by="avg_1_Week_Return", ascending=False).reset_index(drop=True)
        elif period == "1Month":
            df = df_result.sort_values(by="avg_1_Month_Return", ascending=False).reset_index(drop=True)
        elif period == "3Month":
            df = df_result.sort_values(by="avg_3_Month_Return", ascending=False).reset_index(drop=True)
        elif period == "6Month":
            df = df_result.sort_values(by="avg_6_Month_Return", ascending=False).reset_index(drop=True)
        else:
            df = df_result.sort_values(by="avg_1_Year_Return", ascending=False).reset_index(drop=True)

        # st.rerun()
        st.dataframe(df)

    def load_page(self):
        periods = ["1Week", "1Month", "3Month", "6Month", "1Year"]
        period = st.sidebar.selectbox("Select period", periods)

        self.show_results(period)


Results().load_page()