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
import sys

__author__ = 'Kalyan'

app3 = Flask(__name__)
app3.config['TESTING'] = True
UPLOAD_FOLDER = 'C:/Users/kalya_kl8c3da/Documents/GitHub/Flask_api_test/static/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# app.secret_key = '1e1768d1021a1d50162616a2'

@app3.route("/")
def index():
    return render_template("image_upload.html")


@app3.route('/image_upload', methods=['GET', 'POST'])
def image_upload():
    # app = Flask(__name__)
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
    return render_template('image_upload.html')

@app3.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)

@app3.route("/downloadpdffile/<filename>", methods = ['GET'])
def download_pdf_file(filename):
    return render_template('downloadpdf.html',value=filename)


@app3.route("/fruitapi/<filename>", methods=["GET", "POST"])
def fruitapi(filename):
    import cv2
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    from tensorflow.keras.models import load_model

    output_name = os.path.splitext(filename)[0]
    target = os.path.join(APP_ROOT, 'C:/Users/kalya_kl8c3da/Documents/GitHub/Flask_api_test/static/')
    destination = "/".join([target, filename])
    # import cv2
    # cv2.waitKey(1000)
    # cv2.destroyAllWindows()

    # import csv

    try:
        from PIL import Image
    except ImportError:
        import Image


    fruit_names = ['Fresh apple', 'Rotten orange', 'Fresh banana','Rotten banana','Rotten apple', 'Fresh orange' ]
    model = load_model('C:/Users/kalya_kl8c3da/Documents/GitHub/Flask_api_test/static/fruit_model_v1.h5')
    imge = cv2.imread(destination, cv2.IMREAD_COLOR)
    img = cv2.resize(imge,(50, 50))
    img = np.reshape(img,[1, 50, 50,3])
    classes = model.predict(img)
    l = []
    for i in range(len(classes[0])):
        l.append(int(classes[0][i]*100))
    for i in range(len(l)):
        try:
            if l[i] > 90:
                caleb_name = {
                  'Model prediction':{
                      'Id': i,
                      'Name':fruit_names[i],
                      'Confidence': l[i]
                            }
                  }
                json_object = json.dumps(caleb_name, indent =4)
                # print(json_object)
        except:
            if l[i] > 50 or l[i] < 90:
                caleb_name = {
                  'Model prediction':{
                      'Id': i,
                      'Name':fruit_names[i],
                      'Confidence': l[i]
                            }
                  }
                json_object = json.dumps(caleb_name, indent =4)
                # print(json_object)
            elif l[i] < 50:
                print('No Fruit Matched')
    return json_object
    



if __name__ == "__main__":
    app3.run(debug=True)