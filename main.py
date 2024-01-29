from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO
from pymongo import MongoClient
import json
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

configFile = os.path.join(os.path.split(os.path.realpath(__file__))[0],'config.json')
with open(configFile, "r") as json_file:
    data = json.load(json_file)

# MongoDB configuration
MONGO_URI = data['MONGO_URI']
DB_NAME = data['DB_NAME']

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
subscriptions_collection = db['stocks']
users_collection = db['clients']


@app.route('/manage_subscription/<username>', methods=['GET'])
def manage_subscription(username):
    user_document = users_collection.find_one({'username': username})
    return render_template('manage_subscription.html', username=username)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user_document = users_collection.find_one({'username': username})
    if user_document and user_document['password']==password:
        return jsonify({'status': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/')
def index():
    return render_template('login.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
