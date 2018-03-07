# Logging
import logging
import sys
logger = logging.getLogger('spiders_log')
logger.setLevel(logging.DEBUG)

msg_formatter = logging.Formatter("%(asctime)s: %(module)s.py || %(levelname)s - %(message)s")

file_handler = logging.FileHandler('/var/log/plabin/project_snitch/spiders.log')  # Cambiar el directorio
file_handler.setFormatter(msg_formatter)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(msg_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
##

from project_snitch import db
from project_snitch.models import Noticia, EstadoNoticioso, Legislador, FuenteNoticias