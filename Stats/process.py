import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from flask import Flask, jsonify, request
from flask import Flask,jsonify,render_template
import time
import random
global im
im=str(random.randint(1,100000))
n=""
d=""
v=""
winner=""
r=requests.get('http://192.168.43.54:5006/get_chain')
r=r.json()
def func(r):
    global n
    global d
    global v

    n=0
    d=0
    v=0
    r=r['chain']
    for i in r:
        if i['vote']=='Narendra Modi':
            n=n+1
        elif i['vote']=='Vladimir Putin':
            v=v+1
        elif i['vote']=='Donald Trump':
            d=d+1
    return [n,d,v]

y=np.array(func(r))
x=np.array(['Narendra Modi','Donald Trump','Vladimir Putin'])
plt.rcParams['figure.figsize']=(8,5)
fig, ax = plt.subplots( nrows=1, ncols=1 )
ax.bar(x,y)



ax.set_xlabel(xlabel="CANDIDATE",fontsize=15)

ax.set_ylabel(ylabel="VOTES",fontsize=15)

ax.tick_params(labelsize=15)

fig.savefig('static/assets/images/'+im+'.png')
time.sleep(2)
n=func(r)[0]
d=func(r)[1]
v=func(r)[2]

winner=""
if (n>d) and (n>v):
    winner="Narendra Modi"
elif (d>n) and (d>v):
    winner="Donald Trump"
elif (v>n) and (v>d):
    winner="Vladimir Putin"
else:
    winner="Draw"


app=Flask(__name__)

@app.route('/get_stats', methods=['GET'])
def get_stats():
    global n
    global d
    global v
    global winner
    global im



    return render_template('stats.html',n=n,d=d,v=v,winner=winner,im=im)


@app.route('/', methods=['GET'])
def index():
    return render_template('stats.html',n=n,d=d,v=v,winner=winner)

app.run(host='0.0.0.0',port=5010,debug=True)
