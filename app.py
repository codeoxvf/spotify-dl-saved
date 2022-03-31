from flask import Flask, jsonify, request
from requests import request as python_request
from base64 import b64encode
from time import time_ns

from auth.spotifysecret import CLIENT_ID, CLIENT_SECRET


app = Flask(__name__)


@app.route('/')
def index():
    if request.args['code']:
        auth_str = CLIENT_ID + ':' + CLIENT_SECRET
        authorization = b64encode(auth_str.encode()).decode()

        token_response = python_request('POST', 'https://accounts.spotify.com/api/token',
                                        headers={
                                            'Authorization': 'Basic ' + authorization,
                                            'Content-Type': 'application/x-www-form-urlencoded',
                                        }, data={
                                            'grant_type': 'authorization_code',
                                            'code': request.args['code'],
                                            'redirect_uri': request.args['redirect_uri'],
                                        })

        data = token_response.json()

        response_data = {
            'access_token': data['access_token'],
            'refresh_token': data['refresh_token'],
            'expiry': (time_ns() // 1000000) + data['expires_in'],
            'scope': data['scope'],
        }

        response = jsonify(response_data)
        response.headers.add('Access-Control-Allow-Origin',
                             'http://localhost:3000')
        return response
