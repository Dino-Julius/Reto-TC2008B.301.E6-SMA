from flask import Flask, jsonify, request

app = Flask(__name__)

# Inicialmente, las rutas están vacías
routes = []

@app.route('/update_routes', methods=['POST'])
def update_routes():
    global routes
    data = request.get_json()
    routes = data
    print("Rutas actualizadas:", routes)  # Imprimir las rutas actualizadas
    return jsonify({"message": "Routes updated successfully"}), 200

@app.route('/get_routes', methods=['GET'])
def get_routes():
    return jsonify(routes), 200

if __name__ == '__main__':
    app.run(debug=True)