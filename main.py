from app.get_data import SQL
from app.configs import TABLE_PRICE


obj=SQL()

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
    ('volumeTrades', '>', 100000),
]

limit_results = 10

sort_order = ['relatedDate DESC']

result_df = obj.execute_sql_query(
    table_name=TABLE_PRICE,
    columns=columns_to_select,
    filters=filters_to_apply,
    limit=limit_results,
    sort=sort_order
)

print(result_df)