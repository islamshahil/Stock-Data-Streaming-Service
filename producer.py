import os
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

configFile = os.path.join(os.path.split(os.path.realpath(__file__))[0],'config.json')
with open(configFile, "r") as json_file:
    data = json.load(json_file)
    
bootstrap_servers = data['bootstrap_servers']
topic = data['topic']

producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

used_symbols = set()

def generate_stock_data():
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB']
    available_symbols = list(set(symbols) - used_symbols)
    if not available_symbols:
        used_symbols.clear()
        available_symbols = symbols
    symbol = random.choice(available_symbols)
    used_symbols.add(symbol)
    price = round(random.uniform(50, 500), 2)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    stock_data = {
        "name": symbol,
        "price": price,
        "timestamp": timestamp
    }
    return stock_data

while True:
    stock_data = generate_stock_data()
    print(stock_data)
    producer.send(topic, value=str(stock_data).encode('utf-8'))
    print(f"Sent: {stock_data}")
    time.sleep(1)
