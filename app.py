from flask import Flask, request
from scraper import Scraper
from pretty import prettify
from gen import genHTML

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def login():
    return app.send_static_file('login.html')

@app.route('/grades', methods=['POST'])
def grades():
    data = Scraper(request.form['username'], request.form['password']).scrape()

    gradeData = prettify(data)
    return genHTML(gradeData)

@app.route('/test')
def test():
    with open('test.html', 'r') as f:
        data = f.read()
    gradeData = prettify(data)
    return genHTML(gradeData)

@app.route('/style.css')
def style():
    return app.send_static_file('style.css')

@app.route('/grades.js')
def js():
    return app.send_static_file('grades.js')

if __name__ == '__main__':
    app.run()
