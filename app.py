import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
### Utils ###
import configparser

app = Flask(__name__)



app.config.from_object("config.DevelopmentConfig")
print(f'Debug mode set as: {app.config["DEBUG"]}')
print(f'Testing mode set as: {app.config["TESTING"]}')
print(f'App Secret key: {app.config["SECRET_KEY"]}')
print(f'Env set: {app.config["ENV"]}')
print(f'Image uploads set as : {app.config["IMAGE_UPLOADS"]}')
print(f'Session cookie secured: {app.config["SESSION_COOKIE_SECURE"]}')



app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = app.config["IMAGE_UPLOADS"]

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

if __name__ == "__main__":
    app.run(debug=True, port=8080)