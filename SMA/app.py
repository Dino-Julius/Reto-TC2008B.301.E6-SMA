"""
Servidor Flask: Envia el estado de vehículos, semáforos y futuramente peatones en casa paso del sistema via HTTP responde-request.
Diseñado para interactuar con el visualizador 3D en Unity.

Rutas:
    - /start: Obtiene los datos iniciales de los agentes que interactuan en el modelo.
    - /update: Obtiene, por cada paso, los datos de los agentes que interactuan en el modelo.
"""

import os

from flask import Flask, jsonify

from model.environment import CITY, street_directions
from model.model import MovilityModel

# Inicialización del servidor
app = Flask(__name__, static_url_path="")

# Inicialización del modelo
model = MovilityModel(CITY, street_directions, 14, 25)
port = int(os.getenv("PORT", 8585))


@app.route("/start", methods=["GET", "POST"])
def start_model():
    """
    Obtiene los datos iniciales de los agentes que interactuan en el modelo.
    """
    return jsonify(model.start_data())


@app.route("/update", methods=["GET", "POST"])
def update_model():
    """
    Obtiene, por cada paso, los datos de los agentes que interactuan en el modelo.
    """
    model.step()
    return jsonify(model.update_data())


if __name__ == '__main__':
    # Inicialización del servidor
    app.run(host="0.0.0.0", port=port, debug=True)
