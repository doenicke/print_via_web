#!/usr/bin/env python
# coding: utf-8

# flashing: http://flask.pocoo.org/docs/0.12/patterns/flashing/

import os, sys
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask import render_template
from werkzeug.utils import secure_filename
from subprocess import call, check_output

reload(sys)  
sys.setdefaultencoding('utf8')

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
SERVER_PORT=5001

app = Flask(__name__)
app.secret_key = b'*l/fjsd%9feFJ23§$8wr9sjf09'
app.testing = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SERVER_PORT'] = SERVER_PORT


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/index')
@app.route('/')
def index():
    return redirect('/upload')


@app.route('/remove-jobs')
def remove_jobs():
    call(['cancel', '-ax'])
    flash('Druckaufträge gelöscht')
    return redirect('/info')


@app.route('/info')
def printer_info():
    return render_template('printer-info.html', text=check_output(['lpstat', '-t']))


@app.route('/delete/<filename>')
def delete_file(filename):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    error = False
    
    try:
        os.remove(full_path)
    except:
        error = True
        
    if (error):
        flash('Datei konnte nicht gelöscht werden: '+filename)
    else:
        flash('Datei gelöscht: '+filename)

    return redirect(url_for('list_files'))


@app.route('/print/<filename>')
def exec_file(filename):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    error = False
    
    if (not allowed_file(filename)):
        flash('Dateityp ist nicht zum Drucken vorgesehen.')
        return redirect(url_for('list_files'))

    try:
        call(["lp", full_path])
    except:
        error = True
        
    if (error):
        flash('Datei konnte nicht gedruckt werden: '+filename)
    else:
        flash('Datei wurde gedruckt: '+filename)

    return redirect(url_for('list_files'))


@app.route('/show/<filename>')
def show_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=False)   
  

@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['POST'])
def uploader():
    try:
        f = request.files['file']
    except:
        flash('Keine Datei ausgewählt')
        return redirect('/upload')
        
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], 
           secure_filename(f.filename) ))
    flash('Datei gespeichert: '+secure_filename(f.filename))
    return redirect(url_for('list_files'))


@app.route('/list', methods=['GET'])
def list_files():
    files = []
    return render_template('list.html', 
        files=os.listdir(app.config['UPLOAD_FOLDER']) )
        

if __name__ == '__main__':
    app.run(debug=True, port=app.config['SERVER_PORT'], host='0.0.0.0')

