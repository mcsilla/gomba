import json
import redis
from flask import Flask, make_response, abort, redirect
app = Flask(__name__)

MUSHROOM_PREFIX = 'mushroom_'

@app.route('/')
@app.route('/index.html')
def content():
    return redirect("/mushrooms")

@app.route('/image/<image_name>')
def image_route(image_name):
    redis_client = redis.StrictRedis()
    image_bytes = redis_client.get('image_' + image_name)
    if image_bytes is None:
        abort(404)
    response = make_response(image_bytes)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/mushrooms', strict_slashes=False)
def list_mushrooms():
    species_list = []
    redis_client = redis.StrictRedis()
    for key in redis_client.keys(MUSHROOM_PREFIX + '*'):
        mushroom_name_hun = json.loads(redis_client.get(key))['name']['hungarian']
        key_without_prefix = key[len(MUSHROOM_PREFIX):].decode('utf8')
        species_list.append('<li> <a href="/mushrooms/' + key_without_prefix + '">' + mushroom_name_hun + '</a> </li>')
    species_list_str = '\n'.join(species_list)

    return f'''
<!doctype html>

<html lang="hu">
<head>
    <meta charset="utf-8">
    <title>Tanulás</title>
</head>
<body>
    <h1>Gombák</h1>
    <ul>{species_list_str}</ul>
</body>
</html>

'''


@app.route('/mushrooms/<mushroom_key>')
def mushroom_route(mushroom_key):
    redis_client = redis.StrictRedis()
    mushroom_data = redis_client.get(MUSHROOM_PREFIX + mushroom_key)
    if mushroom_data is None:
        abort(404)
    image_name = json.loads(mushroom_data)['images'][0]
    mushroom_name_hun = json.loads(mushroom_data)['name']['hungarian']
    mushroom_name_lat = json.loads(mushroom_data)['name']['latin']
    return f'''
<!doctype html>

<html lang="hu">
<head>
    <meta charset="utf-8">
    <title>Title</title>
</head>
<body>
    <h1>{mushroom_name_hun} ({mushroom_name_lat})</h1>
    <img src="/image/{image_name}" alt="mushroom_name_hun"/>
</body>
</html>

'''


if __name__ == '__main__':
    app.run(debug=True, port=2001, host='0.0.0.0')
