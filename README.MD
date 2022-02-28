# CoinTracker

This bot is made to track prices of cryptocurrencies of your choice.\
The project is based on [NekoGram](https://github.com/lyteloli/NekoGram) and [CoinGecko API](https://www.coingecko.com/en/api/documentation).

## Installation
In order to run a copy of your bot you need 
to do the following:
- Install [Python 3.9+ and pip](https://www.python.org/downloads/)
- Install MySQL or MariaDB
- Install pipenv \(`pip install pipenv`\)
- Clone the project from `https://github.com/lyteloli/CoinTracker.git`
- Run `pipenv install` in your project folder
- Create a .env file as shown below
```dotenv
token = "" # Your Telegram bot token obtained from @BotFather
mysql_password = "" # MySQL password
mysql_db = "coin_tracker" # MySQL database name
mysql_host = "localhost" # MySQL host
mysql_port = 3306 # MySQL port
mysql_user = "root" # MySQL user
```
- \[Optional\] Buy a subscription for [CoinGecko API](https://www.coingecko.com/en/api/pricing)
- Import `coin_tracker.sql` file to your MySQL / MariaDB installation
- Run the project with `pipenv run {python version} main.py`
- 😋 Enjoy!
