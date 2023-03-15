### This script returns the dollar value of a crypto sale on a specific date

from time import strftime
import requests
from bs4 import BeautifulSoup
import datetime

sale_date = datetime.date(2021, 6, 27)
coin = "BTC"
amount_sold = 0.01

year = sale_date.strftime('%Y')
month = sale_date.strftime('%m')
day = sale_date.strftime('%d')

URL = "https://coinmarketcap.com/historical/"+year+month+day
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("tbody")

#Check if coin exists and get its sale value
if results.find("div", string=coin):
    found_coin = results.find("div", string=coin)
    found_coin = found_coin.parent.parent
    
    name = found_coin.find("a", class_="cmc-table__column-name--name cmc-link")
    price = found_coin.find("td", class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price")
    price = price.text.replace("$","").replace(",","")
    sale_value = float(price) * amount_sold

    print(name.text.strip())
    print(f"Price at {sale_date}: ${price}")
    print(f"Amount sold at {sale_date}: {amount_sold}")
    print(f"Value of sale: ${sale_value}")
    print("------------")

else:
    print("error: coin code not found")