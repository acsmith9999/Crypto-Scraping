from flask import Flask, render_template, request
import cryptoHoldValues

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

# @app.route("/values", methods=['POST'])
# def calculate(fromDate,toDate,coins):
#     data = cryptoHoldValues.hold_values(fromDate,toDate,coins)
#     return data

@app.route("/values", methods=['POST'])
def calculate():
    request_data = request.get_json()

    # Extract the fromDate, toDate, and stringArray values
    fromDate = request_data['fromDate']
    toDate = request_data['toDate']
    coins = request_data['coins']

    data = cryptoHoldValues.hold_values(fromDate,toDate,coins)
    return data