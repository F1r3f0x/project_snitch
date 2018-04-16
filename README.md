# Project Snitch #
Sistema que obtiene datos sobre los Senadores y Diputados de Chile y luego sintetiza estos para distribuirlos de forma sencilla a la población. Permite seguir votaciones, asistencia y noticias de los Legisladores.

Project Snitch es desarrollado con Flask y SQLAlchemy.

Esta siendo alojado en http://project-snitch.us-east-2.elasticbeanstalk.com/

Trello Board: https://trello.com/b/0vUCnalk/project-snitch

## Mapa de Proyecto
+ ### forms:
    Formularios para la aplicación Web.
+ ### models:
    Modelos de SQLAlchemy.
+ ### my_tools:
    Herramientas para extraccion de datos anexos y busqueda de texto (deben ser reescritos para usar SQLAlchemy).
+ ### my_utils:
    Funciones de ayuda para la aplicación Web. (a reescribir)
+ ### Sistema:
    Programas para subir y mantener la informacion generada por los scrappers. (deben ser reescritos para usar SQLAlchemy)
+ ### static:
    Elementos estaticos para la aplicación Web (CSS, JS y otros).
+ ### templates:
    Templates de la aplicación.
    
## Dependencias
 #### Python 3.6.3
  - beautifulsoup4 (4.6.0)
  - lxml (4.1.1)
  - Flask (0.12.2)
  - Flask-Admin (1.5.0)
  - Flask-HTMLMin (1.3.1)
  - Flask-SQLAlchemy (2.3.2)
  - flask-msearch (0.1.5)
  - Flask-WTF (0.14.2)
  - requests (2.18.4)
  - mysqlclient (1.3.12)
  - SQLAlchemy (1.2.4)
  - Whoosh (2.7.4)
  - WTForms (2.1)
  - uWSGI (2.0.17)
  
## Diagrama DB
![diagrama db](/design/diagrama_db.png)
  
## Como ejecutar el proyecto:
  - Extraer a "/project_snitch"
  - Crear base de datos y llenar con scripts en "/design"
  - Agregar archivo credenciales.txt en "../project_snitch" (consultar ejemplo_crendenciales.txt)
    
    Formato:
    - db_host
    - db_port
    - db_user
    - db_password
    - secret_key
    - recaptcha_publica
    - recaptcha_privada
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

 
 
Patricio Alejandro Labin Correa (F1r3f0x) - (2017-2018)

GPLv3
