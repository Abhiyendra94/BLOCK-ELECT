import datetime
import hashlib
import json
from flask import Flask, jsonify, request
from flask import Flask,jsonify
import requests
from base64 import (
    b64encode,
    b64decode,
)

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


candidates={"1":'Narendra Modi',"2":"Donald Trump","3":'Vladimir Vladimirovich Putin'}
r=requests.get('http://192.168.43.54:5003/list')
r=r.json()
#r=requests.get('http://192.168.43.54:5003/list')
#r=r.json()
voters=[]
for i in range(r['length']):
    block=[r['list'][i]['private_key'],r['list'][i]['name'],r['list'][i]['age'],r['list'][i]['gender'],r['list'][i]['publickey']]

    voters.append(block)



from uuid import uuid4
from urllib.parse import urlparse
node_address=str(uuid4()).replace('-','')
class Blockchain:
    def __init__(self):
        self.chain = []
        #self.vote=[]
        self.create_block('0','genesis',0,'0',0)
        self.nodes=set()

    def create_block(self,previous_hash,name,age,gender,vote):
        block = {
            "index": len(self.chain)+1,
            'timestamp': str(datetime.datetime.now()),
            "previous_hash": previous_hash,
            "name":name,
            "age":age,
            "gender":gender,
            "vote":vote
        }

        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        digest=SHA256.new()
        digest.update(encoded_block)
        return digest.hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
        return True

    def add_node(self,address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        netwok=self.nodes
        longest_chain=None
        max_length=len(self.chain)
        for nodes in netwok:
            response=requests.get('http://'+node+'/get_chain')
            if response.status_code==200:
                length=response.json()['length']
                chain=response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length=length
                    longest_chain=chain

        if longest_chain:
            self.chain=longest_chain
            return True
        else:
            return False

app=Flask(__name__)
blockchain=Blockchain()


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {
            'message':'The Blockchain is not valid.'
        }
    return jsonify(response), 200

@app.route('/connect_node', methods=['POST'])
def connect_node():
    json=request.get_json()
    nodes=json.get('nodes')
    if nodes is None:
        return 400
    for node in nodes:
        blockchain.add_node(node)
    response={"message":"all nodes connected","nodes":list(blockchain.nodes)}
    return jsonify(response),201

@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'chain replaced by longest','chain':blockchain.chain}
    else:
        response = {
            'message':
            'all good the chain is largest.'
        }
    return jsonify(response), 200

@app.route('/vote', methods=['POST'])
def vote():
    json=request.get_json()
    previous_block = blockchain.get_previous_block()
    previous_hash = blockchain.hash(previous_block)
    candidate = request.form['candidate']
    key = request.form['key']
    name=""
    age=""
    gender=""
    for i in voters:
        if i[0]==key:
            name=i[1]
            age=i[2]
            gender=i[3]

    block = blockchain.create_block(previous_hash,name,age,gender,candidate)
    block = blockchain.get_previous_block()
    hash = blockchain.hash(block)

    response = {'success': hash}
    return jsonify(response), 200


app.run(host='0.0.0.0',port=5006)
