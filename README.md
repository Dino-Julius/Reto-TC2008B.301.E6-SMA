Reto-TC2008B.301.E6-SMA: Reto Modelación de Sistemas Multiagentes con Gráficas Computacionales (Gpo 301, Equipo 6)
========================


Repositorio para la solución del reto para la clase TC2008B.301.E6 sobre Simulación de Multiagentes.

**Integrantes del Equipo 6**: 
- [Jesús Guzmán - A01799257](https://github.com/XxCppSlayerxX)
- [Ulises Jaramillo - A01798380](https://github.com/Ulises-JPx)
- [Sebastián Espinoza - A01750311](https://github.com/Sebastian-Espinoza-25)
- [Julio Vivas - A01749879](https://github.com/Dino-Julius).

## Índice

1. [Descripción del reto](#descripción-del-reto)
2. [Estructura del proyecto](#estructura-del-proyecto)
3. [Descargar el proyecto](#descargar-el-proyecto)

## Descripción del reto

El reto consiste en proponer una solución al problema de movilidad urbana en México, mediante un enfoque que reduzca la congestión vehicular al simular de manera gráfica el tráfico, representando la salida de un sistema multi agentes.

## Estructura del proyecto

```bash
Reto-TC2008B.301.E6-SMA/                    # Carpeta principal del proyecto
├── .gitignore  
├── Actividad-Integradora-1/                # Carpeta principal para las entregas de la Actividad Integradora 1, acceder a la carpeta para más información
│   ├── a01749879-juliovivas/               # Actividad de Julio Vivas
│   ├── a01750311-sebastianespinoza/        # Actividad de Sebastián Espinoza
│   ├── a01798380-ulisesjaramillo/          # Actividad de Ulises Jaramillo
│   └── a01799257-jesusguzman/              # Actividad de Jesús Guzmán
├── SMA/                                    # Carpeta que contiene el modelo en MESA de Movilidad Urbana, acceder a la carpeta para más información
├── Revisión 1 - Equipo 6.pdf               # Documento de la primera entrega del Reto
├── Revisión 2 - Equipo 6.pdf               # Documento de la segunda entrega del Reto
├── Revisión 3 - Equipo 6.pdf               # Documento de la tercera entrega del Reto 
├── SMA_Visualizador_Equipo6.unitypackage   # Paquete de Unity con el visualizador de la simulación
├── LICENSE                          
└── README.md                               # Este documento
```

## Descargar el proyecto

Para descargar y ejecutar el proyecto, sigue estos pasos:

1. Clona el repositorio:
    ```sh
    git clone https://github.com/Dino-Julius/Reto-TC2008B.301.E6-SMA.git
    ```

2. Navega al directorio del proyecto:
    ```sh
    cd Reto-TC2008B.301.E6-SMA
    ```

### Ejecutar modelo con interfaz gráfica en el navegador web:

4. Para ejecutar la simulación, ejecuta el siguiente comando en la terminal:
    ```sh
    python run.py
    ```

5. Desde el navegador se podrá visualizar la simulación en el navegador web. En la ruta:
    ```sh
    http://127.0.0.1:8521/
    ```

6. Desde la interfaz gráfica se puede avanzar, pausar, reiniciar y modificar los parámetros de la simulación.

7. Para detener la simulación, presiona `Ctrl + C` en la terminal.

### Ejecutar el servidor flask para usar el visualizador de Unity:

4. Para ejecutar el servidor, ejecuta el siguiente comando en la terminal:
    ```sh
    python app.py
    ```

5. Desde el navegador o una herramienta de API testing (como Postman o Insomnia), se podrá visualizar el JSON generado por el servidor. En la ruta:
    
    - Esta ruta genera un JSON con la información al momento de la inicialización de los agentes en la simulación.
        ```sh
        http://127.0.0.1:8585/start
        ```

    - Esta ruta genera un JSON con la información al momento de la actualización de los agentes en la simulación, ya que cada petición es un paso en la simulación.
        ```sh
        http://127.0.0.1:8585/update
        ```

6. Para detener el servidor, presiona `Ctrl + C` en la terminal.

> **Nota:** Es requisito que el servidor de flask esté en ejecución antes de ejecutar el visualizador en Unity, si el visualizador en Unity se reinicia, igual se debe reiniciar el servidor.