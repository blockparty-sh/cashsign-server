import os
import requests
import json


from flask import (
    Flask,
    g,
    request,
    render_template,
    jsonify
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/')
    def message():
        return render_template('message.html')

    @app.route('/cashsign-callback')
    def cashsignCallback():
        # contains signed data 
	sigdata = request.args.get('payload')

        if sigdata is None:
            return jsonify({ 'success': False })

        # contains address we signed
	address = request.args.get('address')

        if address is None:
            return jsonify({ 'success': False })


        # here we verify the signed transaction
        # we use ec-slp rpc
        # you could also do this in browser using bitcore-message
        rpc_payload = {
            "method": "verifymessage",
            "params": [
                address,
                sigdata,
                "message that will be signed"
            ],
            "jsonrpc": "2.0",
            "id": 0,
        }

        resp = requests.post('http://user:0yHrDvvXBHT8cccr9G-cRA==@127.0.0.1:7777', json=rpc_payload).json()

        print(resp['error'])
        success = True

        return jsonify({
	    'success': success,
	    'debug': {
                'resp': resp,
		'rpc_payload': rpc_payload,
                'sigdata': sigdata,
                'address': address
	    }
	})

    return app

