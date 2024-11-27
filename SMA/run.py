"""
Este script inicia el servidor de visualización para el modelo de movilidad urbana utilizando Mesa.
El servidor se configura en el módulo `model.server` y se lanza para permitir la visualización de la simulación en un navegador web.
Esto iniciará el servidor en el puerto predeterminado y podrás visualizar la simulación accediendo a `http://localhost:8521` en tu navegador web.
"""

from model.server import server  # noqa


server.launch()
