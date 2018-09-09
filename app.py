#!/usr/bin/env python

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask import render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/johannes/Dokumente/Entwicklung/python/http-upload/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
SERVER_PORT=5001

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SERVER_PORT'] = SERVER_PORT


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/')
# def index():
#     return redirect(url_for('hello'))
#
# @app.route('/hello/')
# def hello(name = None):
#    return render_template('hello.html')

@app.route('/index')
@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['POST'])
def uploader():
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], 
           secure_filename(f.filename) ))
    return render_template('upload-finished.html', 
            filename=secure_filename(f.filename) )


@app.route('/list', methods=['GET'])
def list_files():
    files = []
    return render_template('list.html', 
        files=os.listdir(app.config['UPLOAD_FOLDER']) )


# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)


if __name__ == '__main__':
    app.run(debug=True, port=app.config['SERVER_PORT'])

