from flask import Flask, jsonify, request
import mapgen, view

app = Flask(__name__, static_folder='webapp', static_url_path="/webapp")


@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})

@app.route("/getmap", methods=['POST'])
def getmap():
    
    seed = int(request.form['seed'])
    
    width = int(request.form['width'])
    height = int(request.form['height'])
    wavelength = int(request.form['size'])
    climate_wl = int(request.form['climate_size'])
    
    sea_lvl = int(request.form['sea_lvl']) /50 -1
    shallow_lvl = max(-1, sea_lvl - 0.20)
    mountain_lvl = int(request.form['mountain_lvl']) /50 -1
    summit_lvl = int(request.form['summit_lvl']) /50 -1
    
    cold_lvl = int(request.form['cold_lvl']) /50 -1
    hot_lvl = int(request.form['hot_lvl']) /50 -1
    freeze_lvl = int(request.form['freeze_lvl']) /50 -1
    
    map = mapgen.gen_test(seed=seed, width=width, height=height, wavelength=wavelength, climate_wl=climate_wl, sea_lvl=sea_lvl, shallow_lvl=shallow_lvl, 
                          mountain_lvl=mountain_lvl, summit_lvl=summit_lvl, cold_lvl=cold_lvl, hot_lvl=hot_lvl, freeze_lvl=freeze_lvl)
    map_string = view.maptohtml(map)
    return jsonify({"mapname": 'testmap', "map_string":map_string})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")