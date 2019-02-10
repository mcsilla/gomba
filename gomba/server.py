import base64
import redis
from flask import Flask, make_response, abort
app = Flask(__name__)

@app.route('/index.html')
def content():
    return '''
<!doctype html>

<html lang="en">
<head>
    <meta charset="utf-8">

    <title>Title</title>


</head>

<body>

<img src="image/kucsma_cseh" alt="cseh kucsmagomba" />

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

@app.route('/mushrooms')
def list_mushrooms():
    lista = '' 
     
    redis_client = redis.StrictRedis()
    for key in redis_client.keys():
        if key.startswith(b'mushroom'):
            lista += '<li>' + key.decode('utf8') + '</li>'

    return '''
<!doctype html>

<html lang="hu">
<head>
    <meta charset="utf-8">

    <title>Tanulás</title>


</head>

<body>

<h1>Gombák</h1>

<ul>''' + lista + '''</ul>

</body>
</html>

'''





if __name__ == '__main__':
    app.run(debug=True, port=2001, host='0.0.0.0')
