import os,secrets
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from os import environ
import time,glob
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


    workerSetting = 0
    delay = 0

    # get from env
    if environ.get('WORKER') is not None:
        workerSetting = int(environ.get('WORKER'))
    else:
        workerSetting = 1

    if environ.get('DELAY') is not None:
        delay = int(environ.get('WORKER'))
    else:
        delay = 5

    worker = workerSetting
    currentPID = ""

    workerCounter = len(glob.glob1('./tmp',"*.pid"))

    if workerCounter < worker:
        # create pid and process
        currentPID = "pidof"+secrets.token_hex(5)+".pid"
        f = open("./tmp/"+currentPID, "w")
        f.write(currentPID)
        f.close()

        #simulate long query (5 seconds wait)
        time.sleep(delay)
            
        if 'file' not in request.files:
            return {'msg': 'File Not Found'},400

        file = request.files['file']

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

            # removing the pid
            if currentPID != "" and os.path.exists('./tmp/'+currentPID):
                os.remove("./tmp/"+currentPID)
                print("The file has been deleted successfully")

            # return data to client
            return {'status': "ok","average": result}, 200
    else:
        return {'status': "error","msg":'Worker are Busy, please try again later'}, 400

def processCSV(path):
    #csv = np.genfromtxt(path, delimiter=',' , names=True)
    df = pd.read_csv(path,sep=',')
    numpyresult = df.to_numpy()
    return np.average(numpyresult[:,1])

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')  # run our Flask app