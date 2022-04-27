import numpy as np
import argparse
# import camelot
# import zipfile
import cv2
import io
import numpy
from functools import wraps
import requests
from flask import Flask, request, render_template, send_from_directory, jsonify, Response, url_for, redirect,send_file
import json
# from openpyxl import load_workbook
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
app = Flask(__name__)
app.config['TESTING'] = True
UPLOAD_FOLDER = 'C:/Users/kalya_kl8c3da/Documents/GitHub/projects/Face_recognition_API_dlib/static/'
                
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# db = SQLAlchemy(app)

# class user(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80))
#     email = db.Column(db.String(120))
#     password = db.Column(db.String(80))


# class user(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	degree = db.Column(db.String(100))
# 	branch = db.Column(db.String(100))
# 	year = db.Column(db.Integer)
# 	subject = db.Column(db.String(100))
# 	def __repr__(self):
# 		return 'user' + str(self.id)



@app.route("/")
def index():
    return render_template("image_upload.html")

@app.route('/image_upload', methods=['GET', 'POST'])
def image_upload():

    app = Flask(__name__, template_folder='templates')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # Upload API
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")
            # send file name as parameter to downlad
            return redirect('/downloadfile/' + filename)

@app.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)
@app.route("/downloadpdffile/<filename>", methods = ['GET'])
def download_pdf_file(filename):
    return render_template('downloadpdf.html',value=filename)

names = os.listdir(UPLOAD_FOLDER)
final_name_list = {}
@app.route('/test')
def list_files():
    names = os.listdir(UPLOAD_FOLDER)  
    names = {"Names": names}
    final_name_list = names
    return names
@app.route('/test/name_list', methods=['GET'])

def name_list_jsonify():
    return jsonify(final_name_list)

		# host = '127.0.0.1:5000/face_rec'
        # url = 'http://127.0.0.1:5000/face_rec'
@app.route('/camera')
def camera():
	return render_template('camera3.html')

def compare_image():
	if request.method == 'POST':
		url = 'https://coeaifaceapi.herokuapp.com/face_rec'
		files = {'file': open('filename.jpg', 'rb')}
		resp = requests.post(url, files=files)
		#print(json.dumps(resp.json()))
		return json.dumps(resp.json(), skipkeys = True)
	else:
		return jsonify({'message': 'Something went wrong'})

###################################Create API############################################################
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
#from face_util import compare_faces, face_rec, find_facial_features, find_face_locations
import re
import pdb

app = Flask(__name__)

UPLOAD_FOLDER = 'received_files'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#############face_util################
import face_recognition as fr

def compare_faces(file1, file2):
    """
    Compare two images and return True / False for matching.
    """
    # Load the jpg files into numpy arrays
    image1 = fr.load_image_file(file1)
    image2 = fr.load_image_file(file2)
    
    # Get the face encodings for each face in each image file
    # Assume there is only 1 face in each image, so get 1st face of an image.
    image1_encoding = fr.face_encodings(image1)[0]
    image2_encoding = fr.face_encodings(image2)[0]
    
    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = fr.compare_faces([image1_encoding], image2_encoding)    
    return results[0]

# Each face is tuple of (Name,sample image)    
known_faces = [('Obama','static/obama.jpg'),
               ('Kalyan Mohanty','static/kalyan.jpg'),
               ('Priyanka Pattnaik','static/priyanka.png'),
               ('Barsa Pattnaik','static/barsa.jpg'),
               ('Jaya D Singham','static/jaya.png'),
               ('khirod Behera','static/khirod.png'),
               ('Manas R Mohanty','static/manas.png'),
               ('Priti Sahoo','static/priti.png'),
               ('Smruti S Das','static/smruti.png'),
               ('Susantini Behara','static/susantini.png'),
               ('Prof. Patra','static/principal.jpg'),
               ('Girish','static/pan.jpg')
              ]
    
def face_rec(file):
    """
    Return name for a known face, otherwise return 'Uknown'.
    """
    for name, known_file in known_faces:
        if compare_faces(known_file,file):
            return name
    return 'Unknown' 
    
def find_facial_features(file):
    # Load the jpg file into a numpy array
    image = fr.load_image_file(file)

    # Find all facial features in all the faces in the image
    face_landmarks_list = fr.face_landmarks(image)
    
    # return facial features if there is only 1 face in the image
    if len(face_landmarks_list) != 1:
        return {}
    else:
        return face_landmarks_list[0]
        
def find_face_locations(file):
    # Load the jpg file into a numpy array
    image = fr.load_image_file(file)

    # Find all face locations for the faces in the image
    face_locations = fr.face_locations(image)
    
    # return facial features if there is only 1 face in the image
    if len(face_locations) != 1:
        return []
    else:
        return face_locations[0]        
##############end###############



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/face_match', methods=['POST', 'GET'])
def face_match():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('file1' not in request.files) or ('file2' not in request.files):
            print('No file part')
            return redirect(request.url)

        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        # if user does not select file, browser also submit an empty part without filename
        if file1.filename == '' or file2.filename == '':
            print('No selected file')
            return redirect(request.url)

        if allowed_file(file1.filename) and allowed_file(file2.filename):
            #file1.save( os.path.join(UPLOAD_FOLDER, secure_filename(file1.filename)) )
            #file2.save( os.path.join(UPLOAD_FOLDER, secure_filename(file2.filename)) )
            ret = compare_faces(file1, file2)
            resp_data = {"match": bool(ret)} # convert numpy._bool of ret to bool for json.dumps
            return json.dumps(resp_data)

    # Return a demo page for GET request
    return '''
    <!doctype html>
    <title>Face Match</title>
    <h1>Upload two images</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file1>
      <input type=file name=file2>
      <input type=submit value=Upload>
    </form>
    '''

def print_request(request):
    # Print request url
    print(request.url)
    # print relative headers
    print('content-type: "%s"' % request.headers.get('content-type'))
    print('content-length: %s' % request.headers.get('content-length'))
    # print body content
    body_bytes=request.get_data()
    # replace image raw data with string '<image raw data>'
    body_sub_image_data=re.sub(b'(\r\n\r\n)(.*?)(\r\n--)',br'\1<image raw data>\3', body_bytes,flags=re.DOTALL)
    print(body_sub_image_data.decode('utf-8'))

@app.route('/face_rec', methods=['POST', 'GET'])
def face_recognition():
    if request.method == 'POST':
        # Print request url, headers and content
        print_request(request)

        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files.get('file')
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        if allowed_file(file.filename):
            name = face_rec(file)
            resp_data = {'name': name }

            # get parameters from url if any.
            # facial_features parameter:
            param_features = request.args.get('facial_features', '')
            if param_features.lower() == 'true':
                facial_features = find_facial_features(file)
                # append facial_features to resp_data
                resp_data.update({'facial_features': facial_features})

            # face_locations parameter:
            param_locations = request.args.get('face_locations', '')
            if param_locations.lower() == 'true':
                face_locations = find_face_locations(file)
                resp_data.update({'face_locations': face_locations})

            return json.dumps(resp_data)

    return '''
    <!doctype html>
    <title>Face Recognition</title>
    <h1>Upload an image</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
   app.run(debug = True)