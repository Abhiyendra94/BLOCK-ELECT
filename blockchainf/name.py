from Crypto.PublicKey import RSA
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
from flask import Flask,jsonify
import requests
import Crypto
from Crypto import Random


app=Flask(__name__)
@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']

    return 201


app.run(host='0.0.0.0',port=5003)
