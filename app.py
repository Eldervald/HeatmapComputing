from flask import Flask, request, send_file
from src.api import MapGenerator
import json
import base64
from PIL import Image

app = Flask(__name__)
map_generator = MapGenerator()

# debug
# with open("static/data.json", "r", encoding="utf-8") as file_object:
#     contents = json.loads(file_object.read())
#     # hots = map_generator.calculate_map(contents)
#     image = map_generator.calculate_map(contents)
#     image.save('res/map.png')
#
#     with open("res/map.png", mode="rb") as file:
#         res_bytes = base64.b64encode(file.read())
#         res_string = res_bytes.decode('utf-8')
#     print(res_string)
#     # print(json.dumps([{'coordinates': {'longitude': x, 'latitude': y}, 'weight': hot} for x, y, hot in hots]))


@app.route('/', methods=['POST'])
def searcher_from_post():
    data = json.loads(request.data)
    # with open("static/data.json", "w", encoding="utf-8") as f:
    #      json.dump(data, f)
    image = map_generator.calculate_map(data)

    image.save("res/map.png")
    with open("res/map.png", mode="rb") as file:
        res_bytes = base64.b64encode(file.read())
        res_string = res_bytes.decode('utf-8')
    return json.dumps({'heatmapImageBase64': res_string})

    # post = [{'coordinates': {'longitude': x, 'latitude': y}, 'weight': hot} for x, y, hot in hots]
    # return json.dumps(post)


if __name__ == '__main__':
    app.run(port=5002)
