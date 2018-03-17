"""
    Script para ejecutar spiders

    Esta script se debe ejecutar como una tarea, ya sea con cron o como servicio
    en Windows.

    Para ver un ejemplo funcional, consultar cron_jobs.txt

    Patricio Labin Correa - 2018
    GPLv3
"""

import sys
sys.path.extend(['../../project_snitch'])  # Source Path

from project_snitch.noticias import latercera
latercera.agregar_noticias()

from project_snitch.noticias import rbb
rbb.agregar_noticias()