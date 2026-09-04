from flask import Flask, jsonify
import mapgen, view

app = Flask(__name__, static_folder='webapp', static_url_path="/webapp")


@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})

@app.route("/getmap")
def getmap():
    map = mapgen.gen_test()
    map_string = view.maptohtml(map)
    return jsonify({"mapname": 'testmap', "map_string":map_string})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")