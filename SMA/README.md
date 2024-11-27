SMA en MESA: Modelo de Movilidad Urbana
========================

El modelo de movilidad urbana es un sistema multiagente (SMA) que simula el tráfico de automóviles en una ciudad. La ciudad cuenta con una red de calles, semáforos y estacionamientos. Los autos navegan por la ciudad de manera inteligente, evitando obstáculos y respetando los semáforos.

![Mapa de la ciudad](assets/image.png)

Los estacionamientos se encuentran numerados para poder identificar claramente en cuál estacionamiento tiene que llegar o salir un automovil.

La visualización se ejecuta hasta que los autos (auto) hayan llegado a su destino.

## Índice

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Instrucciones de Simulación](#instrucciones-de-simulación)
3. [Descargar y Ejecutar el Proyecto](#descargar-y-ejecutar-el-proyecto)

## Estructura del Proyecto

```bash
SMA/                                    # Carpeta principal del proyecto
├── assets/                             # Carpeta que contiene los recursos necesarios para la simulación
├── model/                              # Carpeta que contiene el modelo de agentes
├── tests/                              # Carpeta que contiene las pruebas del modelo de agentes
├── app.py                              # Script para ejecutar el servidor 
├── README.md                           # Este documento
├── run.py                              # Script para ejecutar la simulación
└── setup.py                            # Script de configuración de la simulación
```

## Instrucciones de Simulación:

Durante la simulación, se observará lo siguiente:

- El modelo de agentes incluye todos los agentes y objetos necesarios.
- El visualizador permite ver toda la simulación en tiempo real.
- Para cada auto, se puede indicar de manera sencilla el número de estacionamiento del que sale y al que llega.
- Los autos:
    - Navegan inteligentemente por la ciudad.
    - Evaden obstáculos y no colisionan.
    - Respetan los semáforos.
    - Comienan en un estacionamiento inicial y llegan a otro estacionamiento.
- Los semáforos cambian de color de manera adecuada e inteligente.

Estas características aseguran una simulación completa y funcional del sistema multiagente.

## Descargar y Ejecutar el Proyecto:

Para descargar y ejecutar el proyecto, sigue estos pasos:

1. Clona el repositorio:
    ```sh
    git clone https://github.com/Dino-Julius/Reto-TC2008B.301.E6-SMA.git
    ```

2. Navega al directorio del proyecto:
    ```sh
    cd Reto-TC2008B.301.E6-SMA
    cd SMA
    ```

3. Instala las dependencias:
    ```sh
    pip install .
    ```

4. Ejecuta la simulación:
    ```sh
    python run.py
    ```

Esto iniciará el servidor y podrás visualizar la simulación en tu navegador web.