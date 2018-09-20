from flask import Flask, render_template, request, jsonify
import requests




app = Flask(__name__)

@app.route('/keys')
def keys():
    r=requests.get('http://192.168.43.54:5003/list')
    r=r.json()
    voters=[]
    for i in range(r['length']):
        block=[r['list'][i]['private_key'],r['list'][i]['name'],r['list'][i]['age'],r['list'][i]['gender'],r['list'][i]['publickey'],r['list'][i]['aadhar']]

        voters.append(block)


    name=voters[-1][5]
    priv=voters[-1][0]

    pub=voters[-1][4]

    return render_template('keys.html',name=name,priv=priv,pub=pub)

app.run(host='0.0.0.0',port=5005,debug=True)
