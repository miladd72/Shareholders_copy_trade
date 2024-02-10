import pandas as pd
import json
from app.get_data import SQL
from app import df_shareholders_change
from app.configs import TABLE_PRICE

class Strategy:
    def __init__(self):
        self.db = SQL()
        self.shares_diff = df_shareholders_change

    def calculate_returns(self, df):
        # df['Daily_Return'] = df['closePriceAdjust'].pct_change()
        df = df.sort_values(by="relatedDate", ascending=True).reset_index(drop=True)

        df['1_Week_Return'] = df['closePriceAdjust'].pct_change(periods=5).shift(-5)
        df['1_Month_Return'] = df['closePriceAdjust'].pct_change(periods=20).shift(-20)
        df['3_Month_Return'] = df['closePriceAdjust'].pct_change(periods=60).shift(-60)
        df['6_Month_Return'] = df['closePriceAdjust'].pct_change(periods=120).shift(-120)
        df['1_Year_Return'] = df['closePriceAdjust'].pct_change(periods=250).shift(-250)

        return df

    def get_ohlcv(self, name):
        symbol_id = self.shares_diff.loc[self.shares_diff["name"] == name, "symbolId"].iloc[0]

        columns_to_select = [
            'symbolId',
            'relatedDate',
            'closePriceAdjust',
        ]

        filters_to_apply = [
            ('tradeType', '=', 1),
            ('symbolId', '=', symbol_id),
        ]

        sort_order = ['relatedDate DESC']

        result_df = self.db.get_data(
            table_name=TABLE_PRICE,
            columns=columns_to_select,
            filters=filters_to_apply,
            sort=sort_order
        )

        return result_df

    def calculate_average_return(self, df, min_count=3):
        avg_return1 = df['1_Week_Return'].mean() if df['1_Week_Return'].count() > min_count else None
        avg_return2 = df['1_Month_Return'].mean() if df['1_Month_Return'].count() > min_count else None
        avg_return3 = df['3_Month_Return'].mean() if df['3_Month_Return'].count() > min_count else None
        avg_return4 = df['6_Month_Return'].mean() if df['6_Month_Return'].count() > min_count else None
        avg_return5 = df['1_Year_Return'].mean() if df['1_Year_Return'].count() > min_count else None
        count_return1 = df['1_Week_Return'].count()
        count_return2 = df['1_Month_Return'].count()
        count_return3 = df['3_Month_Return'].count()
        count_return4 = df['6_Month_Return'].count()
        count_return5 = df['1_Year_Return'].count()
        df_result = pd.DataFrame({'shareHolderCode': df.shareHolderCode.values[0],
                                  'shareHolderName': df.shareHolderName.values[0],
                                  'stocks': df.name.values[0],
                                  'avg_1_Week_Return': [avg_return1],
                                  'avg_1_Month_Return': [avg_return2],
                                  'avg_3_Month_Return': [avg_return3],
                                  'avg_6_Month_Return': [avg_return4],
                                  'avg_1_Year_Return': [avg_return5],
                                  'count_1_Week_Return': [count_return1],
                                  'count_1_Month_Return': [count_return2],
                                  'count_3_Month_Return': [count_return3],
                                  'count_6_Month_Return': [count_return4],
                                  'count_1_Year_Return': [count_return5]})

        return df_result

    def get_shareholders(self, stock):
        df = self.shares_diff.query("name == @stock")
        # df_feature = FeatureEngineering().calculate_shareholder_features(df)

        cols = ['relatedDate', 'name', 'symbolId', 'shareHolderCode', 'shareHolderName', 'sharePercDiff']
        df_shares = df[cols]
        df_shares = df_shares.query("sharePercDiff > 0")

        return df_shares
    def prepare_date(self, stock):
        df_price = self.get_ohlcv(stock)
        if len(df_price):
            df_price = self.calculate_returns(df_price)

        df_shares = self.get_shareholders(stock)

        df_price["date"] = df_price["relatedDate"].apply(lambda x: pd.to_datetime(x).date())
        df_shares["date"] = df_shares["relatedDate"].apply(lambda x: pd.to_datetime(x).date())

        df = pd.merge(df_price, df_shares, on=["date", "symbolId"], how="inner")
        return df

    def calculate_avg_return_shareholders(self, stock):
        df = self.prepare_date(stock)

        df_result = pd.DataFrame()
        for index, gp in df.groupby('shareHolderCode'):
            df_return = self.calculate_average_return(gp)
            if len(df_return):
                df_result = pd.concat([df_result, df_return], ignore_index=True)

        return df_result

    def main(self):
        stock_list = self.shares_diff.name.unique()
        df_final = pd.DataFrame()
        for stock in stock_list:
            print(stock)
            df_stock = self.calculate_avg_return_shareholders(stock)
            df_final = pd.concat([df_final, df_stock], ignore_index=True)

        df_final.to_csv("result.csv", index=False)
        print("")

if __name__ == "__main__":
    obj = Strategy()
    # df = obj.calculate_avg_return_shareholders("کایگچ")
    obj.main()
    print("")