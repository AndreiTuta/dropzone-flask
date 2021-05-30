import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
### Utils ###
import configparser
### Boto for s3 ###
import boto3

app = Flask(__name__)



app.config.from_object("config.DevelopmentConfig")
print(f'Debug mode set as: {app.config["DEBUG"]}')
print(f'Testing mode set as: {app.config["TESTING"]}')
print(f'App Secret key: {app.config["SECRET_KEY"]}')
print(f'Env set: {app.config["ENV"]}')
print(f'Image uploads set as : {app.config["IMAGE_UPLOADS"]}')
print(f'Session cookie secured: {app.config["SESSION_COOKIE_SECURE"]}')



app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['IMAGE_UPLOADS_PATH'] = app.config["IMAGE_UPLOADS"]
app.config['MEDIA_UPLOADS_PATH'] = app.config["MEDIA_UPLOADS"]

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir('./upload')
    return render_template('index.html', files=files)

@app.route('/submit', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS_IMAGES']:
            return "Invalid image", 400
        filepath = os.path.join(app.config['IMAGE_UPLOADS_PATH'], filename)
        if os.path.exists(filepath):
            return "Image exists", 400
        uploaded_file.save(filepath)
    return '', 204


@app.route('/submit-media', methods=['POST'])
def upload_media_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS_MEDIA']:
            return "Invalid file format", 400
        filepath = os.path.join(app.config['MEDIA_UPLOADS_PATH'], filename)
        if os.path.exists(filepath):
            return "File exists", 400
        uploaded_file.save(filepath)
    return '', 204

@app.route('/uploads/images/<filename>')
def view_image_upload(filename):
    return send_from_directory(app.config['IMAGE_UPLOADS_PATH'], filename)


@app.route('/sync')
def sync_uploads():
    # Creating the low level functional client
    client = boto3.client(
        's3',   
        aws_access_key_id = app.config["AWSID"],
        aws_secret_access_key = app.config["AWSSEC"],
        region_name = app.config["REGION"]
    )

    # Fetch the list of existing buckets
    clientResponse = client.list_buckets()
    
    return render_template('sync.html', buckets=clientResponse['Buckets'])

@app.route('/uploads/media/<filename>')
def view_media_upload(filename):
    return send_from_directory(app.config['MEDIA_UPLOADS_PATH'], filename)

if __name__ == "__main__":
    app.run(debug=True, port=8080)