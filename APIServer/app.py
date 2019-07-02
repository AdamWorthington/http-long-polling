from flask import Flask, jsonify, request, Response
from flask_restful import Resource, Api
from redis import Redis
import time, threading, random, os, json
from flask import session
from functools import wraps

app = Flask(__name__)
api = Api(app)

update_available = threading.Event()
data_available = threading.Event()

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
redis = Redis(host=REDIS_HOST, port=REDIS_PORT)

def valid_credentials(username, password):
    return username == os.environ['USER'] and password == os.environ['PASS']

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth == None or not auth.username or not auth.password or not valid_credentials(auth.username, auth.password):
            return Response('Unauthorized.', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})
        return f(*args, **kwargs)
    return wrapper

class CameraLogs(Resource):
    @authenticate
    def get(self):
        update_available.set()
        data_available.wait()
        data_available.clear()
        b = json.loads(redis.get('buffer'))
        print b
        return jsonify(b)
    
class Updater(Resource):
    def get(self): 
        update_available.wait()
        update_available.clear()
        return "updated"

class LogCollecter(Resource):
    def post(self):
        redis.set('buffer', request.get_json())
        data_available.set()

api.add_resource(CameraLogs, '/logs/')
api.add_resource(Updater, '/updates/')
api.add_resource(LogCollecter, '/dump/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
