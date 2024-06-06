from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = 'QRRX5QLI6T3TIMKI'

def fetch_data_from_alpha_vantage(symbol):
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol.split(":")[1]}&to_symbol={symbol.split(":")[0]}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data from Alpha Vantage: {response.status_code}")
        return None
    return response.json()

def analyze_data(data):
    # Dummy analysis for illustration. Replace with your scalping strategy.
    return {
        "sell": {
            "entry": float(list(data["Time Series FX (Daily)"].values())[0]['4. close']) - 0.001,
            "stop_loss": float(list(data["Time Series FX (Daily)"].values())[0]['4. close']) + 0.002,
            "take_profit": float(list(data["Time Series FX (Daily)"].values())[0]['4. close']) - 0.003
        },
        "buy": {
            "entry": float(list(data["Time Series FX (Daily)"].values())[0]['4. close']) + 0.001,
            "stop_loss": float(list(data["Time Series FX (Daily)"].values())[0]['4. close']) - 0.002,
            "take_profit": float(list(data["Time Series FX (Daily)"].values())[0]['4. close']) + 0.003
        }
    }

@app.route('/predict/<symbol>', methods=['GET'])
def predict(symbol):
    alpha_vantage_data = fetch_data_from_alpha_vantage(symbol)
    if not alpha_vantage_data or 'Time Series FX (Daily)' not in alpha_vantage_data:
        return jsonify({"error": "Data fetch error from Alpha Vantage"})

    analysis = analyze_data(alpha_vantage_data)
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
