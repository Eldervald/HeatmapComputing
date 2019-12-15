from flask import Flask, request
from src.api import MapGenerator
import json

app = Flask(__name__)
map_generator = MapGenerator()


@app.route('/', methods=['POST'])
def searcher_from_post():
    data = json.loads(request.data)

    hots = map_generator.calculate_map(data)

    return json.dumps([{'coordinates': {'longitude': x, 'latitude': y}, 'weight': hot} for x, y, hot in hots])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
