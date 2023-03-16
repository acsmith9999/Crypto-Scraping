### This script calculates values of cryptocurrencies held over a financial year in USD

import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path

# Define date range for financial year (UI)
FY = 2021
#TODO - User selects dates in UI
yearFrom = datetime.date(FY,7,1)
yearTo = datetime.date(FY+1,6,30)
#Assign years to list and create urls
years = [yearFrom, yearTo]
#User selects coins and enters amounts held, assign these to dictionary
coins = {"BTC": 52, "ETH": 0.3, "ADA": 1}
#Store value changes to add up at the end
change_values = []
#create dataframe headers
df = pd.DataFrame(index=range(len(coins)),columns=['Coin Name','Coin Code',f'Price at {yearFrom}',f'Amount held at {yearFrom}',f'Value held at {yearFrom}',f'Price at {yearTo}',f'Amount held at {yearTo}',f'Value held at {yearTo}','Value change'])
df.index = df.index+1

#TODO change currency

#Loop through each coin
for index, coin in enumerate(coins):
    df.iloc[index,1] = coin
    
    #Placeholders for calculating value change later
    value_start = 0
    value_final = 0

    #Loop through years in date range defined
    for jndex, year in enumerate(years):
        URL = "https://coinmarketcap.com/historical/" + year.strftime('%Y%m%d')

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        selector = soup.find("button", class_="sc-243a694b-0 ebfMGX cmc-button cmc-button--color-default")
        

        results = soup.find("tbody")

        #Check if coin exists and get its values
        if results.find("div", string=coin):
            found_coin = results.find("div", string=coin)
            found_coin = found_coin.parent.parent
            
            name = found_coin.find("a", class_="cmc-table__column-name--name cmc-link")
            df.iloc[index,0] = name.text

            price = found_coin.find("td", class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price")
            price = price.text.replace("$","").replace(",","")
            held_value = float(price) * coins[coin]


            if year == yearFrom:
                value_start = held_value
                #print(name.text.strip())
                df.iloc[index,2] = price
                df.iloc[index,3] = coins[coin]
                df.iloc[index,4] = held_value


            # print(f"Price at {year}: ${price}")
            # print(f"Amount held at {year}: {coins[coin]}")
            # print(f"Value held at {year}: ${held_value}")
            # print("------------")

            if year == yearTo:
                value_final = held_value
                value_change = value_final-value_start
                change_values.append(value_change)
                df.iloc[index,5] = price
                df.iloc[index,6] = coins[coin]
                df.iloc[index,7] = held_value
                df.iloc[index,8] = value_change
                #print(f"Value change: ${value_change}")
                #print()

        #If coin does not exist (typo, newly minted, etc.)
        else:
            print("error: coin code not found")


#print(f"Total value change of all coins in FY {yearFrom.strftime('%Y')}-{yearTo.strftime('%Y')}: ${sum(change_values)}")

print(df)

path = "holdValues.csv"
if df is not None:
    if os.path.isfile(path):
        overwrite = input("WARNING: " + path + " already exists! Do you want to overwrite <y/n>? \n ")
        if overwrite == 'y':
            df.to_csv(path)
            print("export replaced")
        elif overwrite == 'n':
            print("export cancelled")
    else:
        df.to_csv(path)
        print("exported")
else:
    print("no data to export")