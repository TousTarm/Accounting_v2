from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Configure MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.accounting

@app.route('/')
def home():
     return render_template('index.j2')


@app.route('/upload', methods=['POST'])
def upload_file():
     if request.method == 'POST':
          if 'file' not in request.files:
               return redirect(request.url)
     file = request.files['file']
     if file.filename == '':
            return redirect(request.url)
     return render_template('data.j2')

@app.route('/data')
def data():
     return render_template('data.j2')

if __name__ == "__main__":
    app.run(debug=True)
