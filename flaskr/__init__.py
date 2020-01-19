import os
import requests
import json
from . import db, settings


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

        message = 'hello world'


        # here we verify the signed transaction
        # we use ec-slp rpc
        # you could also do this in browser using bitcore-message
        rpc_payload = {
            "method": "verifymessage",
            "params": [
                address,
                sigdata,
                message
            ],
            "jsonrpc": "2.0",
            "id": 0,
        }

        RPC_USER = os.getenv('RPC_USER')
        RPC_PASS = os.getenv('RPC_PASS')
        RPC_HOST = os.getenv('RPC_HOST')
        RPC_PORT = os.getenv('RPC_PORT')
        url = 'http://'+RPC_USER+':'+RPC_PASS+'@'+RPC_HOST+':'+RPC_PORT

        print(url)
        resp = requests.post(url, json=rpc_payload).json()

        success = resp['result']

        if success == True:
            print("add user:")
            print(db.add_user(address, message, sigdata))


        return jsonify({
            'success': success,
            'debug': {
                'resp': resp,
                'rpc_payload': rpc_payload,
                'sigdata': sigdata,
                'address': address
            }
        })

    @app.route('/admin')
    def admin():
        return render_template('admin.html', users=db.get_users())

    @app.route('/crowdsale')
    def crowdsale():
        return render_template('crowdsale.html')

    @app.route('/crowdsale-callback')
    def crowdsaleCallback():
        # contains signed data 
        sigdata = request.args.get('payload')

        if sigdata is None:
            return jsonify({ 'success': False })

        # here we verify the signed transaction
        # we use ec-slp rpc
        # you could also do this in browser using bitcore-message
        rpc_payload = {
            "method": "broadcast",
            "params": [
                sigdata
            ],
            "jsonrpc": "2.0",
            "id": 0,
        }

        RPC_USER = os.getenv('RPC_USER')
        RPC_PASS = os.getenv('RPC_PASS')
        RPC_HOST = os.getenv('RPC_HOST')
        RPC_PORT = os.getenv('RPC_PORT')
        url = 'http://'+RPC_USER+':'+RPC_PASS+'@'+RPC_HOST+':'+RPC_PORT

        print(url)
        resp = requests.post(url, json=rpc_payload).json()

        success = resp['result']

        return jsonify({
            'success': success,
            'debug': {
                'resp': resp,
                'rpc_payload': rpc_payload,
                'sigdata': sigdata
            }
        })


    return app

