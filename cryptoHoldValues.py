### This script calculates values of cryptocurrencies held over a financial year where

import datetime
import requests
from bs4 import BeautifulSoup

# Define date range for financial year (UI)
FY = 2021
#TODO - User selects dates in UI
yearFrom = datetime.date(FY,7,1)
yearTo = datetime.date(FY+1,6,30)
#Assign years to list and create urls
years = [yearFrom, yearTo]
#User selects coins and enters amounts held, assign these to dictionary
coins = {"BTC": 52}
#Store value changes to add up at the end
change_values = []

#Loop through each coin
for coin in coins:

    #Placeholders for calculating value change later
    value_start = 0
    value_final = 0

    #Loop through years in date range defined
    #June 27 is the latest date in each FY
    for year in years:
        URL = "https://coinmarketcap.com/historical/" + year.strftime('%Y%m%d')
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find("tbody")

        #Check if coin exists and get its values
        if results.find("div", string=coin):
            found_coin = results.find("div", string=coin)
            found_coin = found_coin.parent.parent
            
            name = found_coin.find("a", class_="cmc-table__column-name--name cmc-link")
            price = found_coin.find("td", class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price")
            price = price.text.replace("$","").replace(",","")
            held_value = float(price) * coins[coin]

            if year == yearFrom:
                value_start = held_value
                print(name.text.strip())

            print(f"Price at {year}: ${price}")
            print(f"Amount held at {year}: {coins[coin]}")
            print(f"Value held at {year}: ${held_value}")
            print("------------")

            if year == yearTo:
                value_final = held_value
                value_change = value_final-value_start
                change_values.append(value_change)
                print(f"Value change: ${value_change}")
                print()

        #If coin does not exist (typo, newly minted, etc.)
        else:
            print("error: coin code not found")


print(f"Total value change of all coins in FY {yearFrom.strftime('%Y')}-{yearTo.strftime('%Y')}: ${sum(change_values)}")
