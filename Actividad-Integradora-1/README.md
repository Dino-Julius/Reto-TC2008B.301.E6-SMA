Actividad Integradora 1 - Equipo 6
========================


Demostrar el conocimiento y aplicación de los conceptos estudiados hasta el momento en el área de Gráficas Computacionales y Sistemas de Multi-Agentes.

**Integrantes del Equipo 6**: 
- [Jesús Guzmán - A01799257](https://github.com/XxCppSlayerxX)
- [Ulises Jaramillo - A01798380](https://github.com/Ulises-JPx)
- [Sebastián Espinoza - A01750311](https://github.com/Sebastian-Espinoza-25)
- [Julio Vivas - A01749879](https://github.com/Dino-Julius).

## Estructura

```bash

Actividad-Integradora-1/            # Carpeta principal para las entregas de la Actividad Integradora 1
├── a01749879-juliovivas/           # Actividad - Gráficas Computacionales de Julio Vivas
├── a01750311-sebastianespinoza/    # Actividad - Gráficas Computacionales de Sebastián Espinoza
├── a01798380-ulisesjaramillo/      # Actividad - Gráficas Computacionales de Ulises Jaramillo
├── a01799257-jesusguzman/          # Actividad - Gráficas Computacionales de Jesús Guzmán
├── SMA/                            # Actividad - Sistemas Multiagente
└── Readme.md                       # Este documento
```

## Descripción de la Actividad Integradora 1

### Sistema Multiagente

El objetvo del reto es que al menos un auto salga de un estacionamiento y llegue a otro.

Para el resto del reto, utilizando el siguiente mapa para una ciudad.

![Mapa de la ciudad](image.png)

Los estacionamientos se encuentran numerados para poder identificar claramente en cuál estacionamiento tiene que llegar o salir un automovil.

La visualización se ejecuta hasta que los autos (auto) hayan llegado a su destino.

### Gráficas Computacionales

### Presentación Individual

Cada integrante debe presentar un archivo con extensión `.unitypackage` que incluya SOLAMENTE lo necesario (quitar todo lo que no sea parte de la entrega, de lo contrario se restarán 10 puntos) para mostrar:

- 1 modelo de automóvil diferente, por integrante del equipo, con materiales y texturas.
- El auto debe ser modelado usando el plugin: ProBuilder.
- La escena en general debe contener (desarrollado por ustedes, o bien descargado de Internet, pero dando crédito y licencia de uso por cada elemento):
    - Al menos 4 ejemplos de texturas.
    - Al menos 4 ejemplos de materiales.
    - Al menos 4 ejemplos de modelos.
    - Al menos 1 ejemplo de semáforo.
    - Al menos 1 ejemplo de camino (asfalto) con señalamientos (línea de rebase, línea continua).
    - Al menos 1 ejemplo de cruce peatonal, señalizado.
    - Al menos 1 ejemplo de banqueta.
    - Al menos 1 ejemplo de edificio.
    - Al menos dos fuentes puntuales de iluminación.
    - El modelo del cruce (la calle) para automóviles. Debe ser lo más cercano posible a la solución final.

La escena no requiere tener funcionalidad. No requiere conexión al servidor de posiciones de IA. Solamente requiere cumplir con los requisitos anteriores, en cuanto a los temas:
- Geometría
- Topología
- Mapeo UV y texturas
- Materiales y colores

## Índice

1. [Instrucciones de Simulación](#instrucciones-de-simulación)
2. [Descargar y Ejecutar el Proyecto](#descargar-y-ejecutar-el-proyecto)

## Instrucciones de Simulación:

Durante la simulación, se observará lo siguiente:

- El modelo de agentes incluye todos los agentes y objetos necesarios.
- El visualizador permite ver toda la simulación en tiempo real.
- Para cada auto, se puede indicar de manera sencilla el número de estacionamiento del que sale y al que llega.
- Los autos:
    - Evaden obstáculos y no colisionan.
    - Respetan los semáforos.
    - Salen y entran en el lugar indicado.
- Los semáforos cambian de color de manera adecuada.

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
    cd Actividad-Integradora-1
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