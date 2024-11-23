from flask import Flask, jsonify, request

app = Flask(__name__)

# Rutas predefinidas para hacer pruebas en unity.
routes = [
    {
        "id": 1,
        "path": [
            {"latitude": 35, "longitude": -45},
            {"latitude": 47, "longitude": -45},
            {"latitude": 47, "longitude": -14},
            {"latitude": 13, "longitude": -14},
            {"latitude": 13, "longitude": -194},
            {"latitude": 45, "longitude": -194},
            {"latitude": 45, "longitude": -205},
            
        ],
    },
    {
        "id": 2,
        "path": [
            {"latitude": 156, "longitude": -205},
            {"latitude": 168, "longitude": -205},
            {"latitude": 168, "longitude": -155},
            {"latitude": 227, "longitude": -155},
            {"latitude": 227, "longitude": -14},
            {"latitude": 135, "longitude": -14},
            {"latitude": 135, "longitude": -24},


           
            
        ],
    },
]

@app.route('/get_routes', methods=['POST'])
def get_routes():
    return jsonify(routes)

if __name__ == '__main__':
    app.run(debug=True)
