# Prueba tecnica lambda BACK

En esta guia se encuentra el proceso de instalación y ejecución del back desarrollado para la prueba tecnica, este backend fue desarrollado con **python**, usando el framework **django**.


# Requisitos

Para el correcto funcionamiento de este proyecto se requiere que se tenga instalado **Python** en su sistema para este proyecto se uso la version **3.12.5**.

## Clonar repositorio

Este repositorio es publico por lo que la clonación es un proceso rápido y sencillo

**clonar repositorio**
`git clone https://github.com/JoseDavidN/prueba_tecnica_lambda.git`

Una vez clonado el repositorio deberemos ubicarnos en dicho directorio atraves de la consola esto lo hacemos con el comando
`cd prueba_tecnica_lambda`

Una vez allí deberemos crear un entorno virtual de python, para esto ejecutamos el comando
`python3 -m venv venv`
o en windows
`python -m venv venv`

Una vez creado el entorno virtual procedemos a activarlo para esto usamos estos comandos
`source venv/bin/activate`
o para windows
`.\venv\Scripts\activate`


## Ejecutar proyecto

Para poder ejecutar nuestro proyecto primero deberemos ejecutar los paquetes o dependencias necesarias para esto ejecutaremos el comando
`pip install -r requirements.txt`

Esto instalara todos las dependencias o paquetes necesarios para el correcto funcionamiento del proyecto, una vez instalados procedemos a ejecutar el proyecto, para esto debemos ubicarnos en la carpeta **APIBACK** y proceder a ejecutar el proyecto, lograremos esto ejecutando los comandos
`cd APIBACK`
`python manage.py runserver`

Esto nos ejecuta el proyecto en el link **http://127.0.0.1:8000**, este el el puerto por defecto en el que se ejecuta **django** el proyecto ya esta configurado para correcto bajo este puerto evite cambiarlo.