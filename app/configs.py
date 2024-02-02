import os

from dotenv import load_dotenv


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv()

USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

SERVER = '172.16.0.22'
DATABASE = 'SFGCOREDATA'

TABLE_PRICE = 'dbo.TcTtHsStOhlcPricesLr'
TABLE_SHARE_HOLDERS = 'dbo.TcTtHsStShareHolders'
TABLE_SYMBOL = 'dbo.Symbol'