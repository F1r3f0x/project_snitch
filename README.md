# Project Snitch #
Sistema que obtiene datos sobre los Senadores y Diputados de Chile y luego sintetiza estos para distribuirlos de forma sencilla a la población. Permite seguir votaciones, asistencia y noticias de los Legisladores.

Project Snitch es desarrollado con Flask y SQLAlchemy.

Esta siendo alojado en https://projectsnitch.ddns.net

## Mapa de Proyecto
+ Application:
    Applicacion web.
+ Datos:
    Datos obtenidos al hacer scrapping (para desarrollo).
+ Noticias:
    Scripts para extraer y subir noticias al sistema.
+ Sistema:
    Scripts para subir y mantener la informacion del sistema
    
## Dependencias
+ Python 3.6.5
  
## Diagrama DB
![diagrama db](/design/diagrama_db.png)
  
## Como ejecutar el proyecto:
  - Inicializar BD
  
        flask db init
  
  - Actualizar con migracion actual
  
        flask db ugpgrade
  
  - Llenar BD con scripts en "/design"
  
  - Setear variables de entorno
    + SNITCH_DB_HOST: Host de DB
    + SNITCH_DB_PORT: Puerto de DB
    + SNITCH_DB_NAME: Nombre de DB
    + SNITCH_DB_USER: Usuario de DB
    + SNITCH_DB_PASS: Contraseña de DB
    + SNITCH_SECRET_KEY: Secret Key para Flask.
    + SNITCH_RECAPTCHA_PUBLIC_KEY: Clave publica de Recaptcha
    + SNITCH_RECAPTCHA_PRIVATE_KEY: Clave privada de Recaptcha
    + FLASK_ENV: Opcion de entorno para flask ("production" o "development")
    + FLASK_APP: (OPCIONAL) Nombre de las script de punto entrada, solo necesaria para el entorno donde se realizan cambios a BD.
  - Ejecutar wsgi.py 
  
        python wsgi.py

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
