from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

FINNHUB_API_KEY = 'cpgvjspr01qp5iv4vi3gcpgvjspr01qp5iv4vi40'

def fetch_data_from_finnhub(symbol):
    url = f'https://finnhub.io/api/v1/forex/candle?symbol={symbol}&resolution=D&count=90&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data from Finnhub: {response.status_code}")
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

    analysis = analyze_data(finnhub_data)
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
