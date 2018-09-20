from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('verify.html')

@app.route('/process', methods=['POST'])
def process():

	key = request.form['key']
	r=requests.get('http://192.168.43.54:5006/get')
	r=r.json()
	block=r[key]




	if block is not {}:
		return jsonify({"success":"your block is verified"})


	return jsonify({'error' : 'Missing data!'})

app.run(host='0.0.0.0',port=5007,debug=True)
