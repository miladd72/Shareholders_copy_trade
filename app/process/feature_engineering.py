import pandas as pd


class FeatureEngineering:
    def __init__(self):
        pass

    @staticmethod
    def calculate_shareholder_features(data):
        individual_shareholders = data[data['shareHolderName'] == "شخص حقیقی"]
        corporate_shareholders = data[data['shareHolderName'] != "شخص حقیقی"]

        individual_features = individual_shareholders.groupby('relatedDate').agg({
            'shareHolderName': 'count',
            'sharePerc': 'sum'
        }).rename(columns={'shareHolderName': 'num_individual_shareholders', 'sharePerc': 'percent_share_individual'})

        corporate_features = corporate_shareholders.groupby('relatedDate').agg({
            'shareHolderName': 'count',
            'sharePerc': 'sum'
        }).rename(columns={'shareHolderName': 'num_corporate_shareholders', 'sharePerc': 'percent_share_corporate'})

        total_shares = data.groupby('relatedDate')['sharePerc'].sum().rename('total_shares')

        features = pd.concat([individual_features, corporate_features, total_shares], axis=1)

        features = features.fillna(0)

        merged_data = pd.merge(data, features, left_on='relatedDate', right_index=True, how='left')

        return merged_data.reset_index(drop=True)