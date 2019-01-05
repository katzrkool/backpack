from flask import Flask, request, jsonify, redirect
from backpack.scraper import Scraper
from backpack.pretty import prettify
from backpack.gen import genHTML
from backpack.autherror import AuthError
from os import path

app = Flask(__name__, static_url_path='/static', static_folder='../static/')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file('login.html')
    elif request.method == 'POST':
        if request.args.get("login") == 'failed':
            return redirect(request.url_root, '307')
        else:
            try:
                data = Scraper(request.form['username'],
                            request.form['password']).scrape()
            except AuthError:
                return redirect('?login=failed', '303')

            gradeData = prettify(data)
            return genHTML(gradeData, request.url_root)


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return app.send_static_file('login.html')
    elif request.method == 'POST':
        try:
            data = Scraper(request.form['username'],
                        request.form['password']).scrape()
        except AuthError:
            return jsonify(['ERROR! Username or password is incorrect'])

        return jsonify(prettify(data))


@app.route('/faq')
def faq():
    return app.send_static_file('faq.html')


@app.route('/test')
def test():
    with open('{}/../resources/test.html'.format(path.dirname(path.realpath(__file__))), 'r') as f:
        data = f.read()
    gradeData = prettify(data)
    return genHTML(gradeData, request.url_root)


if __name__ == '__main__':
    app.run()
