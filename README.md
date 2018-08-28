# MyBackpack Grade API/Site

This project is a Flask API/Scraper that takes a user's MyBackpack credentials, then display's their grades in a prettier interface

See an example below

![Example of grades](screenshots/example.png)

## Installation and Running
To install, run 
`pip -r requirements.txt`

Then, for a development/test server you can just run `app.py`

`python3 app.py`

Navigate to `0.0.0.0:5000` and you should see the login page.

Go to `0.0.0.0:5000/test`, and you will be able to test the parser and html generator without using real data

Do not use the development/test server for deployment! See [Flask Docs](http://flask.pocoo.org/docs/1.0/deploying/) for more

## Contributing/Issues

If you have a suggestion or error, please report it in [the issues](https://github.com/katzrkool/mybackpack/issues)

If you want to contribute, feel free to submit a pull request. I'd appreciate it!