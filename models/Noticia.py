from datetime import datetime
import sqlalchemy.dialects.mysql as mysql
from project_snitch import db
from project_snitch.models.utilitaria.EnviableAJAX import EnviableAJAX
import project_snitch.my_tools.funciones as tools


class Noticia(db.Model, EnviableAJAX):
    """
    Modelo SQLAlchemy de Noticia.

    Attributes:
        id (int): Id de Región.
        titulo (str): Titulo de la Noticia.
        contenido_texto (str): Contenido en texto de la noticia para respaldo.
        url (str): Url a la Noticia original.
        preview_url (str): Url a preview interna de la noticia.
        titulo_buscable (str): Titulo buscable para Whoosh.
        fecha (datetime): fecha de publicacion de la noticia.
        fuente_noticias_id (int): Id de Spider fuente de la noticia.
        activo (bool): Esta activo en el sistema?

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'noticia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(256), nullable=False)
    contenido_texto = db.Column(mysql.MEDIUMTEXT(unicode=True), nullable=True)
    url = db.Column(db.String(1024), nullable=False)
    preview_url = db.Column(db.String(1024), nullable=True)
    titulo_buscable = db.Column(db.String(256), nullable=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now())
    fuente_noticias_id = db.Column(db.Integer,
                                   db.ForeignKey('fuente_noticias.id'),
                                   default=1, primary_key=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self,
                 titulo='Titulo',
                 url='www.project_snitch.cl',
                 **kwargs):
        """
        Args:
            titulo (str): Titulo de la Noticia.
            url (str): Url a la Noticia original.

        Keyword Args:
            contenido_texto (str): Contenido en texto de la noticia para respaldo.
            preview_url (str): Url a preview interna de la noticia.
            fecha (datetime): fecha de publicacion de la noticia.
            fuente_noticias_id (int): Id de Spider fuente de la noticia.
        """
        super(Noticia, self).__init__(**kwargs)

        self.titulo = titulo
        self.contenido_texto = kwargs.get('contenido_texto')
        self.url = url
        self.preview_url = kwargs.get('preview_url')
        self.titulo_buscable = tools.get_texto_buscable(titulo)

        fecha = kwargs.get('fecha')
        if fecha:
            self.fecha = fecha

        fuente_noticias_id = kwargs.get('fuente_noticias_id')
        if fuente_noticias_id:
            self.fuente_noticias_id = fuente_noticias_id

    def __str__(self):
        return f'{self.titulo}:\n{self.contenido_texto}\n'

    def __repr__(self):
        return f'<Noticia {self.id}: {self.titulo}, {self.url}, {self.fecha}>'

    def ajax_dict(self):
        ajax_dict = {
            'label': self.titulo,
            'value': self.id,
            'contenido': self.contenido_texto[:127],
            'url': self.url,
            'fecha': str(self.fecha),
            'fuente_noticias': {
                'nombre': self.fuente.nombre,
                'id': self.fuente.id
            },
        }
        return ajax_dict
