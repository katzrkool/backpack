from flask import Flask, request, jsonify, redirect, abort
from backpack.scraper import Scraper
from backpack.pretty import prettify
from backpack.gen import genHTML
from backpack.errors import AuthError, MyBackpackBrokeError
from os import path, environ
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def strip_personal_info(event, hint):
    # Stripping username and password
    for i in ['username', 'password']:
        if i in event['request']['data']:
            event['request']['data'].pop(i)

    # if it fails during the scraper, there was a chance the payload sent to myBackpack
    # (containing username and password) would be sent (and we don't want that)
    for i in event['exception']['values']:
        i['stacktrace']['frames'] = \
            [destroyFormData(x) for x in i['stacktrace']['frames']]
    return event


def destroyFormData(data: dict) -> dict:
    if 'jsessionid' in data['vars']:
        data['vars'].pop('jsessionid')
    if 'payload' in data['vars']:
        payload = data['vars']['payload']
        if 'form:userId' in payload:
            data['vars']['payload'].pop('form:userId')
        if 'form:userPassword' in payload:
            data['vars']['payload'].pop('form:userPassword')

    return data


# If a sentry URL exists, enable sentry error reporting
if environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        before_send=strip_personal_info,
        dsn=environ.get('SENTRY_DSN'),
        integrations=[FlaskIntegration()]
    )

app = Flask(__name__, static_url_path='/static', static_folder='../static/')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file('login.html')
    elif request.method == 'POST':
        if request.args.get("login") == 'failed':
            return redirect(request.url_root, code=307)
        else:
            try:
                data = Scraper(request.form['username'],
                            request.form['password']).scrape()

                gradeData = prettify(data)
                return genHTML(gradeData, request.url_root)
            except AuthError:
                return redirect('?login=failed', code=303)
            except MyBackpackBrokeError:
                abort(504)


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return app.send_static_file('login.html')
    elif request.method == 'POST':
        try:
            data = Scraper(request.form['username'],
                        request.form['password']).scrape()
        except AuthError:
            return jsonify(['ERROR! Username or password is incorrect']), 401
        except MyBackpackBrokeError:
            return jsonify(['ERROR! MyBackpack didn\' reply in a timely manner.']), 504

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

# Error Handlers below

@app.errorhandler(504)
def backpackError(error):
    return app.send_static_file('errors/504.html'), 504

@app.errorhandler(500)
def internalError(error):
    return app.send_static_file('errors/500.html'), 500

@app.errorhandler(404)
def notFound(error):
    return app.send_static_file('errors/404.html'), 404


if __name__ == '__main__':
    app.run()
