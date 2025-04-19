from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

def fetch_bitcoin_price():
    while True:
        try:
            response = requests.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={'ids': 'bitcoin', 'vs_currencies': 'usd'},
                timeout=10
            )
            data = response.json()
            price = data['bitcoin']['usd']
            socketio.emit('btc_price_update', {'price': price})
        except Exception as e:
            print(f"Помилка при отриманні ціни Bitcoin: {e}")
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    thread = threading.Thread(target=fetch_bitcoin_price)
    thread.daemon = True
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
