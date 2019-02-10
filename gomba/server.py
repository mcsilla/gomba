import base64
import redis
from flask import Flask, make_response, abort
app = Flask(__name__)

@app.route('/index.html')
def content():
    redis_client = redis.StrictRedis()
    image_bytes = redis_client.get("kucsma_cseh")
    image_base64 = base64.b64encode(image_bytes).decode('utf8')
    return '''
<!doctype html>

<html lang="en">
<head>
    <meta charset="utf-8">

    <title>Title</title>


</head>

<body>

<img src="data:image/jpeg;base64,''' + image_base64 + '''" alt="Base 64 encoded!" />

</body>
</html>

'''

@app.route('/image/<image_name>')
def image_route(image_name):
    redis_client = redis.StrictRedis()
    image_bytes = redis_client.get(image_name)
    if image_bytes is None:
        abort(404)
    response = make_response(image_bytes)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=2001, host='0.0.0.0')
