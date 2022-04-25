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

app = Flask(__name__)
app.config['TESTING'] = True
UPLOAD_FOLDER = '/static/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# app.secret_key = '1e1768d1021a1d50162616a2'

@app.route("/")
def index():
    return render_template("tabular.html")


@app.route('/tabular', methods=['GET', 'POST'])
def tabular():
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
    return render_template('tabular.html')

@app.route('/tabularpdf', methods=['GET', 'POST'])
def tabularpdf():
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
      #send file name as parameter to downlad
            return redirect('/downloadpdffile/'+ filename)
    return render_template('tabular.html')



@app.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)

@app.route("/downloadpdffile/<filename>", methods = ['GET'])
def download_pdf_file(filename):
    return render_template('downloadpdf.html',value=filename)

@app.route("/ocrapi/<filename>", methods=["GET", "POST"])
def ocrapi(filename):
    import cv2
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    output_name = os.path.splitext(filename)[0]
    target = os.path.join(APP_ROOT, '/static/')
    destination = "/".join([target, filename])
    import cv2
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    import csv

    try:
        from PIL import Image
    except ImportError:
        import Image
    import pytesseract

    imge = cv2.imread(destination, cv2.IMREAD_COLOR)

    # Convert to gray scale image
    gray = cv2.cvtColor(imge, cv2.COLOR_RGB2GRAY)

    # Simple threshold
    _, thr = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Morphological closing to improve mask
    close = cv2.morphologyEx(255 - thr, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

    # Find only outer contours
    contours, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Save images for large enough contours
    # os.chdir(target)
    areaThr = 20000
    i = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if (area > areaThr):
            i = i + 1
            x, y, width, height = cv2.boundingRect(cnt)
            # image_path =
            cv2.imwrite(os.path.join(target, "saty" + str(i) + ".png"), imge[y:y + height - 1, x:x + width - 1])
    target = os.path.join(APP_ROOT, '/static/')
    destination = "/".join([target, filename])
    output_name = os.path.splitext(filename)[0]
    filename4 = 'saty1.png'
    destination4 = "/".join([target, filename4])
    img = cv2.imread(destination4)
    height, width, _ = img.shape
    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".png", img)
    file_bytes = io.BytesIO(compressedimage)
    result = requests.post(url_api, files={"sample_api.png": file_bytes},
                           data={"apikey": "fd148b59ed88957", "language": "eng"})
    result = result.content.decode('utf-8')
    result = json.loads(result)
    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    cv2.destroyAllWindows()
    return jsonify(text_detected)
    return f(*args, **kwargs)


# return Response(text_detected, mimetype='application/json',
#    headers={"Content-disposition":"attachment;filename={}.{}".format(output_name,"json")})
# return send_from_directory(text_detected, as_attachment=True,filename="{} of api.{}".format(output_name,"json"))
# return jsonify(text_detected)

@app.route("/extract/<filename>", methods=["GET", "POST"])
def extract(filename):
    output_name = os.path.splitext(filename)[0]
    target = os.path.join(APP_ROOT, '/static/')
    destination = "/".join([target, filename])
    import cv2
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    import csv

    try:
        from PIL import Image
    except ImportError:
        import Image
    import pytesseract

    imge = cv2.imread(destination, cv2.IMREAD_COLOR)

    # Convert to gray scale image
    gray = cv2.cvtColor(imge, cv2.COLOR_RGB2GRAY)

    # Simple threshold
    _, thr = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Morphological closing to improve mask
    close = cv2.morphologyEx(255 - thr, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

    # Find only outer contours
    contours, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Save images for large enough contours
    # os.chdir(target)
    areaThr = 20000
    i = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if (area > areaThr):
            i = i + 1
            x, y, width, height = cv2.boundingRect(cnt)
            # image_path =
            cv2.imwrite(os.path.join(target, "saty" + str(i) + ".png"), imge[y:y + height - 1, x:x + width - 1])
    ##########################################################################applying transformation after recognition
    filename3 = 'saty1.png'
    destination3 = "/".join([target, filename3])
    #  destination1 = "/".join([target, "saty1.png"])
    image = cv2.imread(destination3, 0)
    img_binary = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    img_binary = 255 - img_binary  # inverting  the image
    Image_size = 2000
    # length_x,width_y = image.size
    length_x = np.array(image).shape[1]
    width_y = np.array(image).shape[0]
    factor = max(1, int(Image_size // length_x))
    size = factor * length_x, factor * width_y
    kernel_length = 5
    # ernel_length = factor
    # Defining a vertical kernel to detect all vertical lines of image
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # Defining a horizontal kernel to detect all horizontal lines of image
    horizantal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    image_1 = cv2.erode(img_binary, vertical_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_1, vertical_kernel, iterations=3)

    # Use horizontal kernel to detect and save the horizontal lines in a jpg
    image_2 = cv2.erode(img_binary, horizantal_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_2, horizantal_kernel, iterations=3)

    # In[45]:

    # addweighted weighs horizantal and horizantal lines the same
    # bitwise or and bitwise_not for exclusive or and not operations

    # Combine horizontal and vertical lines in a new third image, with both having same weight.
    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)  # Eroding and thesholding the image
    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    thresh, img_vh = cv2.threshold(img_vh, 120, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # threshold binary or otsus binarization(mainly for bimodal)
    # thresh is thresholded value used,next is the thresholded image
    bitxor = cv2.bitwise_xor(image, img_vh)
    bitnot = cv2.bitwise_not(bitxor)
    # The mode cv2.RETR_TREE finds all the promising contour lines and reconstruct
    # s a full hierarchy of nested contours. The method cv2.CHAIN_APPROX_SIMPLE
    # returns only the endpoints that are necessary for drawing the contour line.

    contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def sort_contours(cnts, method="left-to-right"):  # initialize the reverse flag and sort index
        reverse = False
        i = 0  # handle if we need to sort in reverse
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True  # handle if we are sorting against the y-coordinate rather than
        # the x-coordinate of the bounding box
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1  # construct the list of bounding boxes and sort them from top to
        # bottom
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][i],
                                            reverse=reverse))  # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)

    # ###following a top-down approach for sorting contours

    # Sort all the contours by top to bottom.
    contours, boundingBoxes = sort_contours(contours, "top-to-bottom")

    # Creating a list of heights for all detected boxes
    heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]  # Get mean of heights
    mean = np.mean(heights)

    box = []  # Get position (x,y), width and height for every contour and show the contour on image
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if (h < 1000 and w < 1000):
            fimage = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            box.append([x, y, w, h])

    # print(box)

    row = []
    column = []
    j = 0

    for i in range(len(box)):

        if (i == 0):
            column.append(box[i])
            previous = box[i]

        else:
            if (box[i][1] <= previous[1] + mean / 2):
                column.append(box[i])
                previous = box[i]

                if (i == len(box) - 1):
                    row.append(column)

            else:
                row.append(column)
                column = []
                previous = box[i]
                column.append(box[i])

    countcol = 0
    for i in range(len(row)):
        countcol = len(row[i])
        if countcol > countcol:
            countcol = countcol

    count = 0
    for i in range(len(row)):
        count += 1

    # Retrieving the centers and sorting them
    center = [int(row[i][j][0] + row[i][j][2] / 2) for j in range(len(row[i])) if row[0]]
    center = np.array(center)
    center.sort()

    # Regarding the distance to the columns center, the boxes are arranged in respective order
    finalboxes = []
    for i in range(len(row)):
        lis = []
        for k in range(countcol):
            lis.append([])
        for j in range(len(row[i])):
            diff = abs(center - (row[i][j][0] + row[i][j][2] / 4))
            minimum = min(diff)
            indexing = list(diff).index(minimum)
            lis[indexing].append(row[i][j])
        finalboxes.append(lis)

    #
    # #psm:Set Tesseract to only run a subset of layout analysis and assume a certain form of imag
    #
    #
    # 0 = Orientation and script detection (OSD) only.
    # 1 = Automatic page segmentation with OSD.
    # 2 = Automatic page segmentation, but no OSD, or OCR. (not implemented)
    # 3 = Fully aut1matic page segmentation, but no OSD. (Default)
    # 4 = Assume a single column of text of variable sizes.
    # 5 = Assume a single uniform block of vertically aligned text.
    # 6 = Assume a single uniform block of text.
    # 7 = Treat the image as a single text line.
    # 8 = Treat the image as a single word.
    # 9 = Treat the image as a single word in a circle.
    # 10 = Treat the image as a single character.
    # 11 = Sparse text. Find as much text as possible in no particular order.
    # 12 = Sparse text with OSD.
    # 13 = Raw line. Treat the image as a single text line,
    #      bypassing hacks that are Tesseract-specific.

    # #
    #     Specify OCR Engine mode. The options for N are:
    #
    #     0 = Original Tesseract only.
    #     1 = Neural nets LSTM only.
    #     2 = Tesseract + LSTM.
    #     3 = Default, based on what is available.
    #
    #

    # In[ ]:

    # custom_config = r'--oem 3 --psm 6 outputbase digits'

    # In[57]:

    # from every single image-based cell/box the strings are extracted via pytesseract and stored in a list
    outer = []

    for i in range(len(finalboxes)):
        for j in range(len(finalboxes[i])):
            inner = ''
            if (len(finalboxes[i][j]) == 0):
                outer.append(' ')
            else:
                for k in range(len(finalboxes[i][j])):
                    y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], \
                                 finalboxes[i][j][k][3]
                    finalling = bitnot[x:x + h, y:y + w]
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                    border = cv2.copyMakeBorder(finalling, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[0, 255])
                    resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    dilation = cv2.dilate(resizing, kernel, iterations=1)  ##size of foreground object increases
                    erosion = cv2.erode(dilation, kernel, iterations=2)  # Thickness of foreground object decreases
                    out = pytesseract.image_to_string(finalling)
                    if (len(out) == 0):
                        out = pytesseract.image_to_string(erosion, config='--psm 6 --oem 3 -c '
                                                                          'tessedit_char_whitelist=0123456789')
                    inner = inner + " " + out
                outer.append(inner)
    arr = np.array(outer)

    dataframe = pd.DataFrame(arr.reshape(len(row), countcol))

    data = dataframe.style.set_properties(align="left")

    # jsonfiles = json.loads(dataframe.to_json(orient='records'))

    # return render_template('tabular.html', ctrsuccess=jsonfiles)
    return Response(dataframe.to_csv(encoding='utf-8'), mimetype="text/csv",
                    headers={"Content-disposition": " attachment;filename={}.{}".format(output_name, "csv")})

    # print(data)
    from json import JSONEncoder
    class NumpyArrayEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, numpy.ndarray):
                return obj.tolist()
            return JSONEncoder.default(self, obj)

    numpyData = {"array": arr}
    encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
    decodedArrays = json.loads(encodedNumpyData)
    finalNumpyArray = numpy.asarray(decodedArrays["array"])
    # return Response(encodedNumpyData, mimetype='application/json',
    #  headers={"Content-disposition":"attachment;filename={} of self.{}".format(output_name,"json")})


# return render_template('table.html', tables=[dataframe.to_html(classes='data')], titles=dataframe.columns.values)

# In[55]:


#  data.to_excel("temp.xlsx")
# file_name = 'document_template.xltx'
#  wb = load_workbook('temp.xlsx')
# wb.save(file_name, as_template=True)
# return send_from_directory(file_name, as_attachment=True)



@app.route("/pdffile/<filename>", methods=["GET", "POST"])
def pdffile(filename):
    output_name = os.path.splitext(filename)[0]
    target = os.path.join(APP_ROOT, '/static/')
    destination = "/".join([target, filename])
    data = "{name}.{form}".format(name=output_name,form="csv")
    data_zip = "{name}.{form}".format(name=output_name,form="zip")
    tables = camelot.read_pdf(destination, pages="1-end")
    mypath =os.path.join(APP_ROOT,'/')
    final_destination = "/".join([mypath,data])
    final_destination_1 = "/".join([mypath,data_zip])
    #tables.export(final_destination,f="excel")
    #return send_file(final_destination,mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",as_attachment=True)
    tables.export(final_destination, f="csv", compress=True)
    return send_file(final_destination_1,mimetype='application/zip',as_attachment=True)
@app.route("/pdffile1/<filename>", methods=["GET", "POST"])
def pdffile1(filename):
    output_name = os.path.splitext(filename)[0]
    target = os.path.join(APP_ROOT, '/static/')
    destination = "/".join([target, filename])
    data = "{name}.{form}".format(name=output_name,form="xlsx")
    tables = camelot.read_pdf(destination, pages="1-end")
    mypath =os.path.join(APP_ROOT,'/')
    final_destination = "/".join([mypath,data])
    tables.export(final_destination,f="excel")
    return send_file(final_destination,mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",as_attachment=True)
    
if __name__ == "__main__":
    app.run(debug=True)
