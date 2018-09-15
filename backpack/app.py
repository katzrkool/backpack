from flask import Flask, request, jsonify
from backpack.scraper import Scraper
from backpack.pretty import prettify
from backpack.gen import genHTML
from os import path

app = Flask(__name__, static_url_path='/static', static_folder='../static/')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file('login.html')
    elif request.method == 'POST':
        data = Scraper(request.form['username'],
                       request.form['password']).scrape()

        gradeData = prettify(data)
        return genHTML(gradeData, request.url_root)

@app.route('/json', methods=['GET', 'POST'])
def json():
    if request.method == 'GET':
        return app.send_static_file('login.html')
    elif request.method == 'POST':
        data = Scraper(request.form['username'],
                       request.form['password']).scrape()

        return jsonify(prettify(data))

@app.route('/test')
def test():
    with open('{}/../resources/test.html'.format(path.dirname(path.realpath(__file__))), 'r') as f:
        data = f.read()
    gradeData = prettify(data)
    return genHTML(gradeData, request.url_root)

if __name__ == '__main__':
    app.run()
