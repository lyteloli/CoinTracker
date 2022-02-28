from NekoGram.storages.mysql.mysql import MySQLStorage
from dotenv import load_dotenv
from NekoGram import Neko
import os

load_dotenv()

BOT_TOKEN: str = os.getenv('token')
STORAGE: MySQLStorage = MySQLStorage(database=os.getenv('mysql_db', 'coin_tracker'),
                                     host=os.getenv('mysql_host', 'localhost'), port=int(os.getenv('mysql_port', 3306)),
                                     user=os.getenv('mysql_user', 'root'), password=os.getenv('mysql_password'))
NEKO: Neko = Neko(storage=STORAGE, token=BOT_TOKEN)
