from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os,csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
#app.config['UPLOAD_FOLDER'] = 'uploads'

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

        csv_data = []
        stream = file.stream.read().decode("UTF-8").splitlines()
        reader = csv.reader(stream, delimiter=';')
        for row in reader:
            csv_data.append(row)

        data = []
        subtotal = 0
        for row in csv_data[3:]:
            
            new_string = row[2].replace(",",".")
            row[2] = new_string
            subtotal += float(row[2])
            subtotal = int(subtotal)
            formatted_row = [row[1], row[2], row[7], row[14]]#filter
            data.append(formatted_row)

        return render_template('data.j2', data=data, subtotal=subtotal)

@app.route('/data')
def data():
     return render_template('data.j2')

if __name__ == "__main__":
    app.run(debug=True)
