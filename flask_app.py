from flask import Flask, request, jsonify, g, stream_with_context
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import json
import os
from dotenv import load_dotenv

from redis_management import update_redis_data, r

load_dotenv()

app = Flask(__name__)


@app.before_request
def get_userid():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('USER') \
            and auth_header[4:].isdigit() and len(auth_header[4:]) == 3:
        user_digit = int(auth_header[4:])
        g.user_identity = f'USER_{user_digit}'
    else:
        g.user_identity = get_remote_address()


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error=f"Rate Limit Exceeded"), 429


limiter = Limiter(
    key_func=lambda: g.user_identity,
    app=app,
    default_limits=[f"4 per minute"],
    storage_uri=os.environ.get("REDIS_URI"),
    strategy="fixed-window",
)


@app.route('/glov_endpoint', methods=['GET'])
def glov_endpoint():
    # Get the value of the 'stream' parameter from the query string
    stream_param = request.args.get('stream', default='false').lower()

    # Check if the header is present and has the expected format
    if g.user_identity.startswith('USER_'):
        # redis process
        update_redis_data(g.user_identity)

        # Create the response JSON
        response_json = {"message": f"Welcome {g.user_identity}, this is your visit #{r.hget(g.user_identity, 'visit')}",
                         "group": r.hget(g.user_identity, 'group'),
                         "rate_limit_left": r.hget(g.user_identity, 'rate_limit_left'),
                         "stream_seq": 0,
                         }
        
        if stream_param == 'true':
            def generate():
                for i in range(5):
                    response_json["stream_seq"]=i+1
                    yield (json.dumps(response_json) + '\n').encode('utf-8')
                    time.sleep(1)

            return app.response_class(stream_with_context(generate()), content_type='application/json'), 200
        
        elif stream_param == 'false':
            return jsonify(response_json), 200

        else:
            # If the authorization header is missing or has an incorrect format, return an error
            error_json = {"error": "Unvalid Stream Value"}
            return jsonify(error_json), 402

    
    else:
        # If the authorization header is missing or has an incorrect format, return an error
        error_json = {"error": "Unauthorized"}
        return jsonify(error_json), 401


if __name__ == '__main__':
    # for debugging locally
	# app.run(debug=True, host='0.0.0.0',port=5000)
	
	# for production
	app.run(host=os.environ.get("APP_RUN_IP"), port=int(os.environ.get("APP_RUN_PORT")))
