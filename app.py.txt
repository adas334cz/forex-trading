from flask import Flask, jsonify
import requests

app = Flask(__name__)

FINNHUB_API_KEY = 'cpgtk4hr01qpm8ao6hr0cpgtk4hr01qpm8ao6hrg'
ALPHA_VANTAGE_API_KEY = 'QRRX5QLI6T3TIMKI'

def fetch_data_from_finnhub(symbol):
    url = f'https://finnhub.io/api/v1/forex/candle?symbol={symbol}&resolution=D&count=90&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    return response.json()

def fetch_data_from_alpha_vantage(symbol):
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol.split(":")[1]}&to_symbol={symbol.split(":")[0]}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
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
    alpha_vantage_data = fetch_data_from_alpha_vantage(symbol)
    
    if 'c' in finnhub_data:
        analysis = analyze_data(finnhub_data)
    else:
        analysis = {"error": "Data fetch error"}
    
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True)
