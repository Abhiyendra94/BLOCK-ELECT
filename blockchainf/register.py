from Crypto.PublicKey import RSA
import datetime
import hashlib
import json
from flask import Flask, jsonify, request,render_template
from flask import Flask,jsonify
import requests
import Crypto
from Crypto import Random
class people():
    def __init__(self):
        self.list=[]

    def add_person(self,name,age,gender,aadhar):
        random_generator=Random.new().read
        key=RSA.generate(1024,random_generator)
        publickey=key.publickey()
        priv=key
        pub=publickey
        priv=priv.exportKey('PEM')
        pub=pub.exportKey('PEM')
        priv=priv[32:-30].decode("utf-8")
        pub=pub[31:-29].decode("utf-8")


        person={
        "name":aadhar,
        "age":age,
        "gender":gender,
        "private_key":priv,
        "publickey":pub,
        "aadhar":name
        }
        self.list.append(person)
        return len(self.list)-1



app=Flask(__name__)
p=people()

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/keys')
def keys():
	return render_template('keys.html')

@app.route('/list', methods=['GET'])
def list():
    response={'list': p.list, 'length': len(p.list)}
    return jsonify(response), 200

@app.route('/process', methods=['POST'])
def register():
    aadhar=request.form['aadhar']
    name=request.form['name']
    age=request.form['age']
    gender=request.form['gender']
    index=p.add_person(name,age,gender,aadhar)
    priv=p.list[index]['private_key']
    pub=p.list[index]['publickey']
    message={'success':"Thank You!"}
    return jsonify(message),201


'''@app.route('/register', methods=['POST'])
def register():
    json=request.get_json()
    #print(json)
    keys=['name','age','gender']
    if not all (key in json for key in keys):
        return "some elements of transaction missing",400
    index=p.add_person(json["name"],json["age"],json["gender"])
    priv=p.list[index]['private_key']
    pub=p.list[index]['publickey']

    #message={"message":json['name']}
    message={"message":
    "keep private key safe and use it on vote screen and use public key to verify your block",
    "private_key":priv,"publickey":pub}
    return jsonify(message),201'''


app.run(host='0.0.0.0',port=5003,debug=True)
