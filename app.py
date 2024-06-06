from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def fetch_data_from_finnhub(symbol):
    url = f'https://finnhub.io/api/v1/forex/candle?symbol={symbol}&resolution=D&count=90&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data from Finnhub: {response.status_code}")
        return None
    return response.json()

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
            "entry": data['c'][-1] - 0.001,
            "stop_loss": data['c'][-1] + 0.002,
            "take_profit": data['c'][-1] - 0.003
        },
        "buy": {
            "entry": data['c'][-1] + 0.001,
            "stop_loss": data['c'][-1] - 0.002,
            "take_profit": data['c'][-1] + 0.003
        }
    }

@app.route('/predict/<symbol>', methods=['GET'])
def predict(symbol):
    finnhub_data = fetch_data_from_finnhub(symbol)
    if not finnhub_data or 'c' not in finnhub_data:
        return jsonify({"error": "Data fetch error from Finnhub"})
    
    alpha_vantage_data = fetch_data_from_alpha_vantage(symbol)
    if not alpha_vantage_data or 'Time Series FX (Daily)' not in alpha_vantage_data:
        return jsonify({"error": "Data fetch error from Alpha Vantage"})

    analysis = analyze_data(finnhub_data)
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
