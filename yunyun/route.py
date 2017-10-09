
from flask import Flask,render_template,jsonify,request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data_submit',methods=['POST'])
def data_submit():
    return jsonify(request.form) 
