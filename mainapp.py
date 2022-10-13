import os,secrets
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import pandas as pd
import numpy as np


UPLOAD_FOLDER = './tmp'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True
api = Api(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def index():
    return {'msg':"helllo world, you're accessing /"},200

@app.route("/compute", methods=['POST'])
def uploadFiles():

        
    if 'file' not in request.files:
        return {'msg': 'File Not Found'},400

    file = request.files['file']

    print(request.files['file'])

    if file and allowed_file(file.filename):
        #filename = secure_filename(file.filename)

        #generating random filename.csv
        filename = secrets.token_hex(15)+".csv"

        # init the fullpath variable
        fullpath = os.path.join(app.config['UPLOAD_FOLDER'],filename)

        # save file to path
        file.save(fullpath)

        # Processing the CSV
        result = processCSV(fullpath)
        return {'status': "ok","average": result}, 200
    return {'status': "error","msg":'Format Not Supported'}, 400

def processCSV(path):
    #csv = np.genfromtxt(path, delimiter=',' , names=True)
    df = pd.read_csv(path,sep=',')
    print(df)
    numpyresult = df.to_numpy()
    return np.average(numpyresult[:,1])

if __name__ == '__main__':
    app.run()  # run our Flask app