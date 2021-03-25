from flask import Flask, render_template, request, redirect, url_for

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



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(list({app.config["IMAGE_UPLOADS"]})[0] + uploaded_file.filename)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=8080)