### This script calculates values of cryptocurrencies held over a financial year in USD

import datetime
import json
from flask import jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path


def hold_values(fromDate, toDate, coins):
    # Define date range for financial year (UI)
    FY = 2021
    #TODO - User selects dates in UI
    yearFrom = datetime.date(FY,7,1)
    yearTo = datetime.date(FY+1,6,30)
    format = '%Y-%m-%d'
    fromDate = datetime.datetime.strptime(fromDate,format)
    toDate = datetime.datetime.strptime(toDate,format)
    fromDate = datetime.date(fromDate.year,fromDate.month,fromDate.day)
    toDate = datetime.date(toDate.year, toDate.month, toDate.day)
    #Assign years to list and create urls
    dates = [fromDate, toDate]
    coinsDict = {}
    for coin in coins:
        coinsDict[coin['name']] = coin['value']
    #User selects coins and enters amounts held, assign these to dictionary
    #coins = {"BTC": 52, "ETH": 0.3, "ADA": 1}
    #Store value changes to add up at the end
    change_values = []
    #create dataframe headers
    df = pd.DataFrame(index=range(len(coins)),columns=['Coin Name','Coin Code',f'Price at {fromDate}',f'Amount held at {fromDate}',f'Value held at {fromDate}',f'Price at {toDate}',f'Amount held at {toDate}',f'Value held at {toDate}','Value change'])
    df.index = df.index+1

    #TODO change currency

    #Loop through each coin
    for index, coin in enumerate(coinsDict):
        df.iloc[index,1] = coin
        print(coin)
        #Placeholders for calculating value change later
        value_start = 0
        value_final = 0

        #Loop through dates in date range defined
        for jndex, date in enumerate(dates):
            URL = "https://coinmarketcap.com/historical/" + date.strftime('%Y%m%d')

            page = requests.get(URL)

            soup = BeautifulSoup(page.content, "html.parser")

            # TODO change currency
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
                held_value = float(price) * coinsDict[coin]


                if date == fromDate:
                    value_start = held_value
                    #print(name.text.strip())
                    df.iloc[index,2] = price
                    df.iloc[index,3] = coinsDict[coin]
                    df.iloc[index,4] = held_value


                # print(f"Price at {year}: ${price}")
                # print(f"Amount held at {year}: {coins[coin]}")
                # print(f"Value held at {year}: ${held_value}")
                # print("------------")

                if date == toDate:
                    value_final = held_value
                    value_change = value_final-value_start
                    change_values.append(value_change)
                    df.iloc[index,5] = price
                    df.iloc[index,6] = coinsDict[coin]
                    df.iloc[index,7] = held_value
                    df.iloc[index,8] = value_change
                    #print(f"Value change: ${value_change}")
                    #print()

            #If coin does not exist (typo, newly minted, etc.)
            else:
                print("error: coin code not found")


    #print(f"Total value change of all coins in FY {yearFrom.strftime('%Y')}-{yearTo.strftime('%Y')}: ${sum(change_values)}")

    print(df)



    return df.to_html()


def export_csv(data):
    path = "holdValues.csv"

    if data is not None:
        if os.path.isfile(path):
            overwrite = input("WARNING: " + path + " already exists! Do you want to overwrite <y/n>? \n ")
            if overwrite == 'y':
                data.to_csv(path)
                print("export replaced")
            elif overwrite == 'n':
                print("export cancelled")
        else:
            data.to_csv(path)
            print("exported")
    else:
        print("no data to export")
