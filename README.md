Twitter sentiment analysis API
=================

API with Flask, Flask-RESTful and
Flask-RESTful-Swagger

Usage
-----

Clone the repo:

    git clone https://github.com/rikardv/twitter-sentiment-api
    cd twitter-sentiment-api

First time installation:

    pip3 install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    python3 setup.py develop # or install if you prefer

Run the sample server

    python3 runserver.py

Try the endpoints:

    curl -XGET http://localhost:5000/dummy
    curl -XPOST -H "Content-Type: application/json" http://localhost:5000/hello -d '{"name": "World"}'
    curl -XPOST -H "Content-Type: application/json" http://localhost:5000/sentiment -d '{"tag": "#ElonMuskIsATroll"}'

Swagger docs available at `http://localhost:5000/api/spec.html`


License
-------

MIT, see LICENSE file

