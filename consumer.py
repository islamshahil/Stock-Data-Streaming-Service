import os
import json
from kafka import KafkaConsumer
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


configFile = os.path.join(os.path.split(os.path.realpath(__file__))[0],'config.json')
with open(configFile, "r") as json_file:
    data = json.load(json_file)

bootstrap_servers = data['bootstrap_servers']
topic = data['topic']

@socketio.on('connect')
def handle_connect():
    print('Client connected')

def store_to_db(stock_data):
    # Implement your logic to store data in the database
    pass

def kafka_consumer():
    try:
        consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, group_id='stock_consumer', auto_offset_reset='earliest')
        for message in consumer:
            stock_data = eval(message.value.decode('utf-8'))
            #print(f"Received: {stock_data}")
            store_to_db(stock_data)
            socketio.emit('stock_data', stock_data)
    except Exception as e:
        print(e)
    finally:
        consumer.close()

if __name__ == '__main__':
    socketio.start_background_task(target=kafka_consumer)
    socketio.run(app, host='0.0.0.0', port=5001, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
