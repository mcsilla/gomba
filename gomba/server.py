import json
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
    image_bytes = redis_client.get('image_' + image_name)
    if image_bytes is None:
        abort(404)
    response = make_response(image_bytes)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/mushrooms')
def list_mushrooms():

    species_list = []
    species_li_tags = [] 
     
    redis_client = redis.StrictRedis()
    for key in redis_client.keys(b'mushroom*'):
        species_list.append('<li>' + json.loads(redis_client.get(key))['name']['hungarian'] + '</li>')
        species_li_tags.append('<li>' + key.decode('utf8') + '</li>')
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
    mushroom_data = redis_client.get('mushroom_' + mushroom_key)
    if mushroom_data is None:
        abort(404)
    image_name = json.loads(mushroom_data)['images'][0]
    return f'''
<!doctype html>

<html lang="hu">
<head>
    <meta charset="utf-8">
    <title>Title</title>
</head>
<body>
    <img src="/image/{image_name}" alt="cseh kucsmagomba" />
</body>
</html>

'''


if __name__ == '__main__':
    app.run(debug=True, port=2001, host='0.0.0.0')
