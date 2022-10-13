import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import pandas as pd
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './tmp'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True
api = Api(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Index(Resource):
    def get(self):
        data = pd.read_csv('users.csv')  # read local CSV
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK

    def post(self):
        data = request.json
        print(request.json)
        if 'file' not in request.files:
            return {'msg': 'No files found'}, 400
        
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            # return jsonify(data)
            return {'msg':'file uploaded'}, 200

api.add_resource(Index, '/compute')  # add endpoints

if __name__ == '__main__':
    app.run()  # run our Flask app