from project_snitch import db


class FuenteNoticias(db.Model):
    """
    Modelo SQLAlchemy de Fuente de Noticias.

    Attributes:
        id (int): Id de Fuente de Noticias.
        nombre (str): Nombre de Fuente.
        url (str): Url de la pagina de noticias que escanea el spider.
        spider_extraccion (str): Nombre de la script spider.
        actvio (bool): Esta activo en el sistema?

        noticias (list[Noticia]): Lista de noticias extraidas por el spider.

        __tablename__: SQLAlchemy variable. Nombre de la tabla en la BD.
    """

    __tablename__ = 'fuente_noticias'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(256), nullable=False)
    spider_extraccion = db.Column(db.String(1024), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    noticias = db.relationship('Noticia', backref='fuente')

    def __init__(self,
                 nombre='Nombre Fuente',
                 url='pagina.cl',
                 spider_extraccion='/scripts/pagina.py',
                 **kwargs):
        """
        Args:
            nombre (str): Nombre de Fuente.
            url (str): Url de la pagina de noticias que escanea el spider.
            spider_extraccion (str): Nombre de la script spider.
        """
        super(FuenteNoticias, self).__init__(**kwargs)

        self.nombre = nombre
        self.url = url
        self.spider_extraccion= spider_extraccion

    def __str__(self):
        return f'{self.nombre} - {self.url}'

    def __repr__(self):
        return f'<FuenteNoticias {self.id}: {self.nombre}, {self.url}, {self.spider_extraccion}'
