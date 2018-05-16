# Project Snitch #
Sistema que obtiene datos sobre los Senadores y Diputados de Chile y luego sintetiza estos para distribuirlos de forma sencilla a la población. Permite seguir votaciones, asistencia y noticias de los Legisladores.

Project Snitch es desarrollado con Flask y SQLAlchemy.

Esta siendo alojado en http://projectsnitch.ddns.net

Trello Board: https://trello.com/b/0vUCnalk/project-snitch

## Mapa de Proyecto
+ ### application
    Applicacion web.
+ ### datos:
    Datos obtenidos al hacer scrapping (para desarrollo).
+ ### noticias:
    Scripts para extraer y subir noticias al sistema.
+ ### sistema:
    Scripts para subir y mantener la informacion del sistema
    
## Dependencias
+ Python 3.6.5
+ MariaDB 10.2.12
  
## Diagrama DB
![diagrama db](/design/diagrama_db.png)
  
## Como ejecutar el proyecto:
  - Crear base de datos y llenar con scripts en "/design"
  - Setear variables de entorno
    + SNITCH_DB_HOST: Host de DB
    + SNITCH_DB_PORT: Puerto de DB
    + SNITCH_DB_NAME: Nombre de DB
    + SNITCH_DB_USER: Usuario de DB
    + SNITCH_DB_PASS: Contraseña de DB
    + SNITCH_SECRET_KEY: Secret Key para Flask.
    + SNITCH_RECAPTCHA_PUBLIC_KEY: Clave publica de Recaptcha
    + SNITCH_RECAPTCHA_PRIVATE_KEY: Clave privada de Recaptcha
  - Ejecutar debug.py 
  
        python debug.py

## Estructura JSONs

+ ### senadores.json
    - **tipo**: Tipo de Legislador
    - **primer_nombre**: Primer nombre. (str)
    - **segundo_nombre**: Segundo nombre. (str)
    - **primer_apellido**: Primer Apellido. (str)
    - **segundo_apellido**: Segundo Apellido. (str)
    - **id_interna**: id interna de la pagina del Senado. (int)
    - **link**: url al perfil del Senador en la pagina del Senado. (str)
    - **telefono**: Teléfono del Senador. (str)
    - **email**: Email del Senador. (str)
    - **region**: Nombre de Región del Senador. (str)
    - **circunscripcion**: Numero Circunscripción del Senador. (str)
    - **partido**: Nombre de Partido del Senador. (str)

+ ### diputados.json
    - **tipo**: Tipo de Legislador
    - **primer_nombre**: Primer nombre. (str)
    - **segundo_nombre**: Segundo nombre. (str)
    - **primer_apellido**: Primer Apellido. (str)
    - **segundo_apellido**: Segundo Apellido. (str)
    - **id_interna**: id interna de la pagina de la camara de diputados. (int)
    - **link**: url al perfil del diputado en la pagina de la camara (str)
    - **telefono**: Teléfono. (str)
    - **email**: Email. (str)
    - **region**: Nombre de Región. (str)
    - **partido**: Nombre de Partido. (str)
    - **distrito**: Distrito (int)

 
<hr>
Patricio Alejandro Labin Correa (F1r3f0x) - (2017-2018)

GPLv3
