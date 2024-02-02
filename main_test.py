import pandas as pd
import pyodbc

# SQL Server connection parameters
server = '172.16.0.22'
database = 'SFGCOREDATA'
username = 'ssrs_test'
password = '1qaz@WSX'

# Create a connection string
conn_str = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

# SQL query
query_shareholders = '''
SELECT 
[relatedDate],
[shareHolderCode],
[cisinShare],
[shareQuantity],
[sharePerc],
[shareHolderName],
[shareQuantityYest],
[sharePercYest],
[symbolId],
[symbolHistoryId]
FROM dbo.TcTtHsStShareHolders
WHERE tradeType = 1
'''

query_symbol = '''
SELECT *
FROM dbo.SymbolHistory
'''

query_price = '''
SELECT
[volumeTrades],
[valueTrades],
[symbolId],
[relatedDate],
[symbolHistoryId],
[closePriceAdjust],
[highPriceAdjust],
[lastPriceAdjust],
[lowPriceAdjust],
[openPriceAdjust],
[yestPriceAdjust]
FROM dbo.TcTtHsStOhlcPricesLr
WHERE tradeType = 1
'''



# Connect to the SQL Server
conn = pyodbc.connect(conn_str)

# Execute the query and fetch results into a DataFrame
df = pd.read_sql_query(query_symbol, conn)

# Save the DataFrame to a CSV file
# df.to_csv('price.csv', index=False)
df.to_csv('SymboleHistory.csv', index=False)

# Close the connection
conn.close()
