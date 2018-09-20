import datetime
import hashlib
import json
from flask import Flask, jsonify, request
from flask import Flask,jsonify,render_template
import requests
from base64 import b64decode
import time
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from base64 import b64decode,b64encode


candidates={"1":'Narendra Modi',"2":"Donald Trump","3":'Vladimir Vladimirovich Putin'}
r=requests.get('http://192.168.43.54:5003/list')
r=r.json()
#r=requests.get('http://192.168.43.54:5003/list')
#r=r.json()
signatures={}
hashes={}
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
        self.create_block('0','genesis',0,'0',0,0)
        self.nodes=set()

    def create_block(self,previous_hash,aadhaar,age,gender,vote,publickey):
        block = {
            "index": len(self.chain),
            'timestamp': str(datetime.datetime.now()),
            "previous_hash": previous_hash,
            "aadhaar":aadhaar,
            "age":age,
            "gender":gender,
            "vote":vote,
            "publickey":publickey
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

    def hasher(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        digest=SHA256.new()
        digest.update(encoded_block)
        return digest

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            block_index += 1
        return True

    def add_node(self,address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        netwok=self.nodes
        longest_chain=None
        max_length=len(self.chain)
        for node in netwok:
            response=requests.get(f'http://{node}/get_chain')
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
@app.route('/', methods=['GET'])
def index():
    return render_template('votes.html')



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

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200

@app.route('/vote', methods=['POST'])
def vote():
    #json=request.get_json()
    #r1=requests.get('http://192.168.43.173:5008/replace_chain')
    previous_block = blockchain.get_previous_block()
    previous_hash = blockchain.hash(previous_block)
    candidate = request.form['candidate']
    key = request.form['key']

    name=""
    age=""
    gender=""
    r=requests.get('http://192.168.43.54:5003/list')
    r=r.json()
    #r=requests.get('http://192.168.43.54:5003/list')
    #r=r.json()
    voters=[]
    for i in range(r['length']):
        block=[r['list'][i]['private_key'],r['list'][i]['name'],r['list'][i]['age'],r['list'][i]['gender'],r['list'][i]['publickey']]

        voters.append(block)
    #a=0
    for i in range (len(voters)):
        x=voters[i][0]
        x=x.replace("\n",r"\n")
        key=key.replace("\n",r"\n")

        #response = {'success':x }
        #return jsonify(response), 200
        if x==key:


            name=voters[i][1]
            age=voters[i][2]
            gender=voters[i][3]
            publickey=voters[i][4]

            block = blockchain.create_block(previous_hash,name,age,gender,candidate,publickey)
            block = blockchain.get_previous_block()
            hasher = blockchain.hasher(block)
            hash=blockchain.hash(block)

            voters.append(x)

        #a=a+1

            #key='MIICWwIBAAKBgQDHZTLtYFWARs/YlkmsrFaX0wnUdyUmmeYvbHFLsSodEA+Ne9Gd\nqh0PkqwOrgpXWYXnYBpxEBXomR8wVwvCO7l2HhQ7jbH0aV1IgPzR0pbJlxk5/TfN\n5/fA6wS9b5c5IRDsco7idwGZZig1ItllGNgeEuYEwS5NXjT+rEZ5TKotxwIDAQAB\nAoGAAIqj0sU6Njj7A4mU9aUaLxthoXQZY7tzRpmyzRPUG3QZtrapYRY/MfWiBgAv\nAwG5PWGjcL8scA9KaGU0IPjsjgZXqSbLHmn4CO4WGNDVJDx3p3xtfGIsmfz/JPlN\nZQ+bqVDnZ9gfB4Q+iZs4dDyiF/mbxTKXLcCyjC7427e0SPECQQDQQzgx6263jb2n\nQu5/C235wfbNBOq8W/R/7jzK9D+CprUD+BIae6wxtf8OA77rkmMKhFWmYlv3UTHU\n0N0+vHE9AkEA9RmmqQyyJxkJPOxdrMY5qQEJitiNXfecGOtmHOpc2cfPEYGaY+Ve\nbeV7douknPoRwNZ1Dr/xlHr7jg0RLZDDUwJAcsJnp9JUyx52wEE4jJcuva6tIaIw\n+yQsoYYUx705dfQI0SwURbWaWDYyWnWj8clTfAsZ6zpN9QUv0VZaY+SQ/QJAZld4\nnJvdg6/TiKnVj4ARsXzqZBx6IuNyPYGFWMuPS6w/zTqFofKzVEX/IIe8i4NriE7E\nAA2rrOkRQsY4BwOsWwJAc6Glsm++QX3sWElw6/4S2dPP1bMnRH6lDjjf8/2asjD7\nr9ShnkADrJ3/gGK5QqA67UfBitaz/kLQkANoPLCrrg=='
            hashes.update({hash:block})
            k=voters[i][0]
            key = b64decode(k)
            keyPriv = RSA.importKey(key)
            signer = PKCS1_v1_5.new(keyPriv)
            sig = signer.sign(hasher)
            sigma=str(sig)
            signatures.update({sigma:block})
            response = {'success':hash}
            #r1=requests.get('http://192.168.43.173:5008/replace_chain')
            return jsonify(response), 200



            #age=i[2]
            #gender=i[3]
            #block = blockchain.create_block(previous_hash,name,age,gender,candidate)
            #block = blockchain.get_previous_block()
            #hash = blockchain.hash(block)

#@app.route('/verify', methods=['GET'])
#def verify():
#    i=signatures['''b'\x13\xa6\x80\xefe>&"bt\x12#\xef&\xae]_\xb6\x1aQ\xe6@\x1dT\xe6\xe4\xdfR\xe7\xe0\xd2\xad\xb3a\xa7\xa0Y{"\xccN\xbf\x7f\xd2\x88\x04v\x10\xe5;\xc7*\xcb\x06\xc9.h\xa0\xab\xba\x15\xf9\xf4\xb3"\x06\xa7\xe5\xc6b\xed\xf4\xd8\x84\x04{\xf1\x95\xf3A\x9c=:/\xb8\xa7\xca\x85|y\x1e8\xed\xcbq\x84\xdb\xcb\t\xf70+\x90eG`\xaf\xa5hMs\n\xc7\n-\xd1qs[\xf0\xde\xc1\xca\xc1_\x9c)\x8e''''][1]
#    return str(i)

@app.route('/public', methods=['GET'])
def public():
    #signature=b64encode(signatures)
    return jsonify(signatures)


@app.route('/get', methods=['GET'])
def get():
    #signature=b64encode(signatures)
    return jsonify(hashes)




app.run(host='0.0.0.0',port=5006,debug=True)
